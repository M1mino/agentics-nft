import { getHttpEndpoint } from "@orbs-network/ton-access";
import { TonClient, WalletContractV4 } from "ton";
import { mnemonicToPrivateKey } from "ton-crypto";

(async () => {
    const MNEMONIC = (process.env.SEED || "").split(" ");
    const endpoint = await getHttpEndpoint({ network: "testnet" });
    const client = new TonClient({ endpoint });
    const key = await mnemonicToPrivateKey(MNEMONIC);
    const wallet = WalletContractV4.create({ publicKey: key.publicKey, workchain: 0 });
    const walletContract = client.open(wallet);
    const bal = await walletContract.getBalance();
    console.log("Address:", walletContract.address.toString());
    console.log("Balance:", bal.toString(), "(nanoTON)");
    console.log("Balance TON:", Number(bal) / 1e9);
})();
