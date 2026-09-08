#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const version = process.argv[2];
if (!version) {
  console.error("Usage: sync-plugin-version.js <version>");
  process.exit(1);
}

const pluginJsonPath = path.join(
  __dirname,
  "..",
  "plugins",
  "foundations",
  ".claude-plugin",
  "plugin.json"
);

const raw = fs.readFileSync(pluginJsonPath, "utf8");
const pluginJson = JSON.parse(raw);
pluginJson.version = version;

fs.writeFileSync(pluginJsonPath, JSON.stringify(pluginJson, null, 2) + "\n");

console.log(`Updated ${pluginJsonPath} to version ${version}`);
