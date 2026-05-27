import { beginCell, toNano, Address } from "ton";
import { NetworkProvider } from '@ton-community/blueprint';
import { NftCollection } from "../wrappers/NftCollection";

export async function run(provider: NetworkProvider) {
    const OFFCHAIN_CONTENT_PREFIX = 0x01;
    const METADATA_BASE_URL = "https://archetypebots.com/metadata/";
    let newContent = beginCell().storeInt(OFFCHAIN_CONTENT_PREFIX, 8).storeStringRefTail(METADATA_BASE_URL).endCell();

    let owner = provider.sender().address!;

    let collection = provider.open(await NftCollection.fromInit(owner, newContent, {
        $$type: "RoyaltyParams",
        numerator: 50n,  // 5% royalty
        denominator: 1000n,
        destination: owner,
    }));

    console.log("Deploying collection at:", collection.address);
    
    // Deploy the collection contract
    await collection.send(provider.sender(), {value: toNano("0.1")}, "Mint");

    await provider.waitForDeploy(collection.address);
    
    console.log("Collection deployed!");
    console.log("Collection address:", collection.address.toString());
    console.log("Owner address:", owner.toString());
    console.log("Max supply: 1000");
    console.log("Mint price: 29 TON");
    console.log("Mint window: 14 days");
    console.log("Transfer lock: 30 days from mint");
    console.log("Metadata URL:", METADATA_BASE_URL);

    // IMPORTANT: After deploy, owner MUST call "StartMint" to open the mint window
    console.log("");
    console.log("⚠️  Next step: call 'StartMint' to begin the 14-day mint window");
    console.log("   await collection.send(provider.sender(), {value: toNano('0.01')}, 'StartMint');");
}
