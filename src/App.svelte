<script>
  import { TezosToolkit, PollingSubscribeProvider } from "@taquito/taquito";
  import { b58cencode, hex2buf, prefix } from '@taquito/utils';

  const rpcUrl = "https://ghostnet.ecadinfra.com";
  const Tezos = new TezosToolkit(rpcUrl);
  const contractAddress = "KT1AJ6EjaJHmH6WiExCGc3PgHo3JB5hBMhEx";

  let text = "Waiting for first event";

  const addressFromBytes = (addressBytes) => {
    const buf = hex2buf(addressBytes);
    const address = b58cencode(buf, prefix.tz1);
    return address;
  }

  Tezos.setStreamProvider(
    Tezos.getFactory(PollingSubscribeProvider)({
      shouldObservableSubscriptionRetry: true,
      pollingIntervalMilliseconds: 1500,
    }),
  );

  try {
    const sub = Tezos.stream.subscribeEvent({
      // tag: "tagName",
      address: contractAddress,
    });

    sub.on("data", (data) => {
      console.log(data);
      const addressBytes = data.payload.args[1].bytes;
      const address = addressFromBytes(addressBytes);
      console.log(address);
      text = "Called by " + address;
    });
  } catch (e) {
    console.log(e);
  }
</script>

<main>
  <h1>Event receiver</h1>

  <div>
    <p>{text}</p>
  </div>
</main>

<style>
</style>
