import "./structs";
import "./messages";

contract NftItem {

    const minTonsForStorage: Int = ton("0.03");
    const gasConsumption: Int = ton("0.03");
    const lockDuration: Int = 30 * 86400;   // 30 days in seconds
    
    collection_address: Address;
    item_index: Int; 
    owner: Address;
    individual_content: Cell;
    is_initialized: Bool;
    mint_time: Int;  // 0 = not minted yet, >0 = unix timestamp of mint

    init(collection_address: Address, item_index: Int, owner: Address, individual_content: Cell, mint_time: Int){
        self.collection_address = collection_address;
        self.item_index = item_index;
        self.owner = collection_address;
        self.individual_content = individual_content;
        self.is_initialized = false;
        self.mint_time = mint_time;
    }

    receive(msg: Transfer){
        let ctx: Context = context();
    
        let msgValue: Int = ctx.value; // Check the gasCost for storage
        let tonBalanceBeforeMsg: Int = myBalance() - msgValue;
        let storageFee: Int = self.minTonsForStorage - min(tonBalanceBeforeMsg, self.minTonsForStorage);
        msgValue = msgValue - (storageFee + self.gasConsumption);

        // Only Owner can transfer
        require(ctx.sender == self.owner, "not owner");

        if (self.is_initialized == false) {  // Initial Transfer, aka the "Minting" of the NFT
            self.is_initialized = true;
            self.owner = msg.new_owner;
            self.mint_time = now();  // record mint timestamp
            send(SendParameters{
                to: msg.response_destination,
                value: 0,
                mode:  SendIgnoreErrors + SendRemainingValue,
                body: Excesses { query_id: msg.query_id }.toCell()
            });
        } else {
            // Time-lock: 30 days must have passed since mint
            require(now() - self.mint_time >= self.lockDuration, "transfer locked for 30 days from mint");
            
            self.owner = msg.new_owner; // change current owner to the new_owner
            if (msg.forward_amount > 0) {
                send(SendParameters{
                    to: msg.new_owner,
                    value: msg.forward_amount,
                    mode: SendIgnoreErrors, 
                    bounce: false,
                    body: OwnershipAssigned{
                        query_id: msg.query_id,
                        prev_owner: ctx.sender,
                        forward_payload: msg.forward_payload
                    }.toCell()
                }); 
            }
            msgValue = msgValue - ctx.readForwardFee(); 
            if (msg.response_destination != null) { 
                send(SendParameters{ 
                    to: msg.response_destination,
                    value: msgValue - msg.forward_amount,
                    mode: SendPayGasSeparately,
                    body: Excesses { query_id: msg.query_id }.toCell()
                });
            } 
        }
    }
    
    receive(msg: GetStaticData){ 
        let ctx: Context = context();
        send(SendParameters {
            to: ctx.sender,
            value: 0,
            mode: 64,  // (return msg amount except gas fees) 
            bounce: true,
            body: ReportStaticData{
                query_id: msg.query_id,
                index_id: self.item_index,
                collection: self.collection_address
            }.toCell()
        });
    }

    // --------- Get Function  --------- //
    get fun get_nft_data(): GetNftData {
        let b: StringBuilder = beginString();
        let collectionData: String = self.individual_content.asSlice().asString();
        b.append(collectionData);
        b.append(self.item_index.toString());
        b.append(".json");

        return GetNftData {
            is_initialized: self.is_initialized, 
            index: self.item_index, 
            collection_address: self.collection_address, 
            owner_address: self.owner,
            individual_content: b.toCell()
        };
    }

    get fun get_mint_time(): Int {
        return self.mint_time;
    }

    get fun is_transfer_locked(): Bool {
        if (self.is_initialized == false) {
            return true;  // not minted yet
        }
        return now() - self.mint_time < self.lockDuration;
    }

    get fun get_seconds_until_unlock(): Int {
        if (self.is_initialized == false) {
            return 0;
        }
        let elapsed: Int = now() - self.mint_time;
        if (elapsed >= self.lockDuration) {
            return 0;
        }
        return self.lockDuration - elapsed;
    }
}
