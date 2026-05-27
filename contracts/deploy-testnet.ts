import { getHttpEndpoint } from "@orbs-network/ton-access";
import { TonClient, WalletContractV4, beginCell, toNano, internal } from "ton";
import { mnemonicToPrivateKey } from "ton-crypto";
import { NftCollection } from "./wrappers/NftCollection";

const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

async function callWithRetry<T>(fn: () => Promise<T>, retries = 5): Promise<T> {
    for (let i = 0; i < retries; i++) {
        try { return await fn(); }
        catch (e: any) {
            if (i === retries - 1) throw e;
            console.log(`  Retry ${i+1}/${retries}: ${e.message?.slice(0, 60)}`);
            await delay(4000);
        }
    }
    throw new Error("unreachable");
}

async function main() {
    const MNEMONIC = (process.env.SEED || "").split(" ");
    if (MNEMONIC.length < 24) throw new Error("Set SEED");

    console.log("Connecting to testnet...");
    const endpoint = await callWithRetry(() => getHttpEndpoint({ network: "testnet" }));
    const client = new TonClient({ endpoint });
    await delay(3000);

    const key = await mnemonicToPrivateKey(MNEMONIC);
    const wallet = WalletContractV4.create({ publicKey: key.publicKey, workchain: 0 });
    const walletContract = client.open(wallet);

    console.log("Wallet:", walletContract.address.toString());

    const bal = await callWithRetry(() => walletContract.getBalance());
    console.log("Balance:", Number(bal) / 1e9, "TON");
    if (bal === 0n) { console.error("Zero balance!"); process.exit(1); }

    const content = beginCell().storeInt(0x01, 8).storeStringRefTail("https://archetypebots.com/metadata/").endCell();
    const owner = walletContract.address;

    const collection = await NftCollection.fromInit(owner, content, {
        $$type: "RoyaltyParams", numerator: 50n, denominator: 1000n, destination: owner,
    });

    console.log("Collection address:", collection.address.toString());

    if (!collection.init) throw new Error("No init");

    const seqno = await callWithRetry(() => walletContract.getSeqno());
    console.log("Seqno:", seqno);

    const transfer = walletContract.createTransfer({
        seqno,
        secretKey: key.secretKey,
        messages: [internal({
            to: collection.address,
            value: toNano("0.1"),
            init: collection.init,
            body: "Mint",
            bounce: false,
        })]
    });

    await callWithRetry(() => walletContract.send(transfer));
    console.log("Deploy tx sent! Waiting...");

    for (let i = 0; i < 30; i++) {
        await delay(4000);
        const dep = await client.isContractDeployed(collection.address).catch(() => false);
        if (dep) {
            console.log("\n✅ Deployed!");
            console.log("Address:", collection.address.toString());
            console.log("Testnet: https://testnet.tonscan.org/address/" + collection.address.toString());
            process.exit(0);
        }
        process.stdout.write(".");
    }
    console.log("\n❌ Timeout. Check: https://testnet.tonscan.org/address/" + collection.address.toString());
}

main().catch(e => {
    console.error("\n❌ Error:", e.message?.slice(0, 150) || e);
    process.exit(1);
});
