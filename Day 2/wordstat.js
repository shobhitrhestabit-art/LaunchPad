#!/usr/bin/env node
// wordstat.js
// Usage: node wordstat.js --file corpus.txt --top 10 --minLen 5 --unique

const fs = require("fs");
const path = require("path");

// --- Step 1: Parse command line arguments ---
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith("--")) {
    const key = args[i].replace("--", "");
    const value = args[i + 1] && !args[i + 1].startsWith("--") ? args[i + 1] : true;
    options[key] = value;
  }
}


const file = options.file || "corpus.txt";
const top = parseInt(options.top) || 10;
const minLen = parseInt(options.minLen) || 1;
const unique = !!options.unique;


if (!fs.existsSync(file)) {
  console.error(` File not found: ${file}`);
  process.exit(1);
}

const text = fs.readFileSync(file, "utf-8");


const words = text
  .toLowerCase()
  .match(/\b[a-z']+\b/g) // only words
  .filter(w => w.length >= minLen);


const counts = {};
for (const word of words) {
  counts[word] = (counts[word] || 0) + 1;
}


let entries = Object.entries(counts);
if (unique) {
  
  entries = entries.filter(([_, count]) => count === 1);
}


entries.sort((a, b) => b[1] - a[1]);


const longestWord = words.reduce((a, b) => (b.length > a.length ? b : a), "");
const shortestWord = words.reduce((a, b) => (b.length < a.length ? b : a), longestWord);

const stats = {
  totalWords: words.length,
  uniqueWords: entries.length,
  longestWord,
  shortestWord,
  topWords: entries.slice(0, top),
};

console.log(`📊 Top ${top} words (minLen=${minLen}, unique=${unique}):`);
console.log("-------------------------------------------");
for (const [word, count] of entries.slice(0, top)) {
  console.log(`${word.padEnd(15)} → ${count}`);
}
console.log("-------------------------------------------");
console.log(`Total words processed: ${words.length}`);
console.log(`Unique words: ${entries.length}`);
console.log(`Longest word: ${longestWord}`);
console.log(`Shortest word: ${shortestWord}`);


fs.mkdirSync("output", { recursive: true });
fs.writeFileSync("output/stats.json", JSON.stringify(stats, null, 2));
console.log(`Stats written to output/stats.json`);
