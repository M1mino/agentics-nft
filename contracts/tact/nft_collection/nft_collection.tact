import "./structs";
import "./messages";
import "./../nft_item/nft_item";

contract NftCollection {
    
    const minTonsForStorage: Int = ton("0.03");
    const gasConsumption: Int = ton("0.03");
    const defaultMintPrice: Int = ton("29");   // 29 TON
    const mintDuration: Int = 14 * 86400;       // 14 days in seconds

    next_item_index: Int as uint32 = 0;
    owner_address: Address;
    royalty_params: RoyaltyParams;                      
    collection_content: Cell;
    mint_price: Int;
    max_supply: Int;
    mint_start_time: Int;  // 0 = mint not started, >0 = unix timestamp of start
    rarity_map: map<Int, RarityInfo>;  // item_index → rarity tier

    init(owner_address: Address, collection_content: Cell, royalty_params: RoyaltyParams){
        self.owner_address = owner_address;
        self.collection_content = collection_content; 
        self.royalty_params = royalty_params;
        self.mint_price = self.defaultMintPrice;
        self.max_supply = 1000;
        self.mint_start_time = 0;
    }

    receive("Mint"){
        let ctx: Context = context();
        let msgValue: Int = ctx.value;

        require(msgValue >= self.mint_price, "insufficient TON for mint");
        require(self.next_item_index < self.max_supply, "max supply reached");
        require(self.mint_start_time > 0, "mint not started");
        require(now() - self.mint_start_time <= self.mintDuration, "mint period ended");

        let tonBalanceBeforeMsg: Int = myBalance() - msgValue;
        let storageFee: Int = self.minTonsForStorage - min(tonBalanceBeforeMsg, self.minTonsForStorage);
        msgValue = msgValue - (storageFee + self.gasConsumption);

        // Send excess back to sender
        let excess: Int = msgValue - ton("0.1"); // reserve for NFT deploy
        if (excess > 0) {
            send(SendParameters{
                to: ctx.sender,
                value: 0,
                mode: SendPayGasSeparately + SendIgnoreErrors,
                body: Excesses{ query_id: 0 }.toCell()
            });
        }

        self.mint(ctx.sender, msgValue);
    }

    // Admin: start mint — sets the 14-day window
    receive("StartMint") {
        require(context().sender == self.owner_address, "only owner");
        require(self.mint_start_time == 0, "mint already started");
        self.mint_start_time = now();
    }

    // Admin: set new mint price
    receive(msg: SetMintPrice) {
        require(context().sender == self.owner_address, "only owner");
        self.mint_price = msg.new_price;
    }

    // Admin: withdraw collected TON
    receive("Withdraw") {
        require(context().sender == self.owner_address, "only owner");
        send(SendParameters{
            to: self.owner_address,
            value: 0,
            mode: SendPayGasSeparately + SendRemainingValue,
            body: Excesses{ query_id: 0 }.toCell()
        });
    }

    // ===== Private Methods ===== //
    fun mint(sender: Address, msgValue: Int) {
        require(self.next_item_index >= 0, "non-sequential NFTs");
        
        // Random rarity assignment: 5% Leg, 15% Epic, 30% Rare, 50% Common
        let r: Int = randomInt(1000);  // 0..999
        let tier: Int;
        if (r < 50) {           // 0-49   = 5%  → Legendary (3)
            tier = 3;
        } elseif (r < 200) {    // 50-199 = 15% → Epic (2)
            tier = 2;
        } elseif (r < 500) {    // 200-499 = 30% → Rare (1)
            tier = 1;
        } else {                // 500-999 = 50% → Common (0)
            tier = 0;
        }
        self.rarity_map.set(self.next_item_index, RarityInfo{ tier: tier });

        let nft_init: StateInit = self.getNftItemInit(self.next_item_index);
        send(SendParameters{
                to: contractAddress(nft_init), 
                value: msgValue, 
                bounce: false,
                mode: SendIgnoreErrors,
                body: Transfer {
                    query_id: 0,
                    new_owner: sender,
                    response_destination: self.owner_address,
                    custom_payload: emptyCell(),
                    forward_amount: 0,
                    forward_payload: emptySlice()
                }.toCell(),
                code: nft_init.code,
                data: nft_init.data
            });
        self.next_item_index = self.next_item_index + 1;
    }

    receive(msg: GetRoyaltyParams) {   
        let ctx: Context = context();
        send(SendParameters{
            to: ctx.sender,
            value: 0,
            mode: 64, 
            bounce: false,
            body: ReportRoyaltyParams {
                query_id: msg.query_id,
                numerator:  self.royalty_params.numerator,
                denominator: self.royalty_params.denominator,
                destination: self.owner_address
            }.toCell()
        });        
    }

    // ------------------ Get Function  ------------------ //
    get fun get_collection_data(): CollectionData {     
        let b: StringBuilder = beginString();
        let collectionDataString: String = self.collection_content.asSlice().asString();
        b.append(collectionDataString);
        b.append("collection.json");
        return CollectionData{
            next_item_index: self.next_item_index, 
            collection_content: b.toCell(), 
            owner_address: self.owner_address
        };
    }

    get fun get_nft_address_by_index(item_index: Int): Address?{      
        let initCode: StateInit = self.getNftItemInit(item_index);
        return contractAddress(initCode);
    }

    get fun getNftItemInit(item_index: Int): StateInit {
        return initOf NftItem(myAddress(), item_index, self.owner_address, self.collection_content, 0);
    }
    
    get fun get_nft_content(index: Int, individual_content: Cell): Cell { 
        let b: StringBuilder = beginString();
        let ic: String = individual_content.asSlice().asString();
        b.append(ic);
        b.append(index.toString());
        b.append(".json");
        return b.toCell();
    }

    get fun royalty_params(): RoyaltyParams {
        return self.royalty_params;
    }

    get fun get_mint_price(): Int {
        return self.mint_price;
    }

    get fun get_max_supply(): Int {
        return self.max_supply;
    }

    get fun get_minted_count(): Int {
        return self.next_item_index;
    }

    get fun get_mint_start_time(): Int {
        return self.mint_start_time;
    }

    get fun get_mint_duration(): Int {
        return self.mintDuration;
    }

    get fun is_mint_active(): Bool {
        return self.mint_start_time > 0 && now() - self.mint_start_time <= self.mintDuration;
    }

    // Rarity getters
    get fun get_rarity(item_index: Int): Int {
        let info: RarityInfo? = self.rarity_map.get(item_index);
        if (info == null) {
            return -1;  // not minted yet
        }
        return info!!.tier;
    }

    get fun get_rarity_name(item_index: Int): String {
        let info: RarityInfo? = self.rarity_map.get(item_index);
        if (info == null) {
            return "unknown";
        }
        let t: Int = info!!.tier;
        if (t == 3) { return "Legendary"; }
        elseif (t == 2) { return "Epic"; }
        elseif (t == 1) { return "Rare"; }
        else { return "Common"; }
    }

    get fun get_rarity_distribution(): String {
        let legendaries: Int = 50;   // 5% of 1000
        let epics: Int = 150;        // 15%
        let rares: Int = 300;        // 30%
        let commons: Int = 500;      // 50%  
        return "L:" + legendaries.toString() + " E:" + epics.toString() + " R:" + rares.toString() + " C:" + commons.toString();
    }
}
