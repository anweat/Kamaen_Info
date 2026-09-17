// Small, reproducible Java Edition (big-endian, gzip) NBT fixture. No save files are touched.
import { gzipSync, gunzipSync } from "node:zlib";
import { writeFile, readFile } from "node:fs/promises";
const str = (value) => {
  const b = Buffer.from(value, "utf8"),
    n = Buffer.alloc(2);
  n.writeUInt16BE(b.length);
  return Buffer.concat([n, b]);
};
const named = (type, name, payload) =>
  Buffer.concat([Buffer.from([type]), str(name), payload]);
const int = (value) => {
  const b = Buffer.alloc(4);
  b.writeInt32BE(value);
  return b;
};
const double = (value) => {
  const b = Buffer.alloc(8);
  b.writeDoubleBE(value);
  return b;
};
const compound = (name, tags) =>
  named(10, name, Buffer.concat([...tags, Buffer.from([0])]));
const raw = compound("", [
  named(3, "schema_version", int(1)),
  named(8, "purpose", str("toolchain_smoke_test")),
  compound("sample", [
    named(6, "frequency", double(0.6)),
    named(3, "observations", int(0)),
    named(8, "stage", str("draft")),
  ]),
]);
const file = new URL("../art/nbt/development-sample.nbt", import.meta.url);
if (process.argv.includes("--check")) {
  if (!gunzipSync(await readFile(file)).equals(raw))
    throw Error("NBT fixture differs from the defined sample");
  console.log("NBT gzip / big-endian fixture verified");
} else {
  await writeFile(file, gzipSync(raw), { flag: "wx" });
  console.log("Created development-sample.nbt");
}
