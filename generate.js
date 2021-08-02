const fs = require('fs');

let teams = new Set(),
  conts = [],
  tableData = [],
  scores = {};

let teamStats = {};

function load(contest) {
  teamStats[contest] = {};
  conts.push(contest);
  let data = JSON.parse(fs.readFileSync(`./contests/${contest}.json`));
  let probCount = 0;
  let acc = {}
  while (String.fromCharCode(probCount + 'A'.charCodeAt(0)) in data[0].detail) {
    acc[String.fromCharCode(probCount + 'A'.charCodeAt(0))] = 0;
    probCount++;
  }

  for (let item of data) {
    for (let prob in item.detail) {
      if (item.detail[prob].time != -1)
        acc[prob] += 1;
    }
  }

  let cnt200 = 0;

  for (let i in data) {
    if (i == "200")
      break;

    let item = data[i];
    for (let prob in item.detail) {
      if (item.detail[prob].time != -1)
        cnt200 += 1;
    }
  }


  const buptHDU = {
    "team0436": "0xCCCCCCCC",
    "team0421": "Harmony",
    "team0438": "asdf2",
    "team0422": "",
    "team0439": "NMLPC",
    "team0432": "",
    "team0433": "不死吃了",
    "team0434": "needone",
    "team0423": "",
    "team0424": "我与肚肚势不两立",
    "team0440": "",
    "team0425": "Burn_Horse",
    "team0426": "莱鸡",
    "team0427": "team-1",
    "team0435": "FPE",
    "team0428": "",
    "team0429": "三只蒟蒻_threekonjaks",
    "team0430": "混到极致便是C",
    "team0437": "无main之王"
  }
  let hi = -1;
  for (let i in data) {
    let item = data[i];
    let cnt = 0;
    for (let prob in item.detail) {
      if (item.detail[prob].time != -1)
        cnt += 1;
    }
    let score = Math.max(0, cnt / cnt200 * (500 - parseInt(item.rank)));
    if (hi == -1)
      hi = score;
    score = score / hi * 100;
    if (contest.indexOf("hdu") != -1) {
      item.school = (item.name.split('   '))[1];
      item.name = (item.name.split('   '))[0];
      if (item.name in buptHDU)
        item.name = buptHDU[item.name];
      if (item.name == "Harmony")
        console.log(item, score);
    }
    if (item.school == "北京邮电大学") {
      teams.add(item.name);
      teamStats[contest][item.name] = `${item.rank}/${cnt}/${score.toFixed(2)}`;
      let found = false;
      for (let t of tableData)
        if (t.name == item.name) {
          found = true;
          // t.data.push(score);
          scores[item.name].push(score);
          if (item.name == "Harmony")
            console.log(t.data);
        }
      if (!found) {
        scores[item.name] = [];
        for (let i = 0; i < conts.length - 1; ++i)
          scores[item.name].push(0);
        scores[item.name].push(score);
        tableData.push({ "name": item.name, "type": "line", "data": scores[item.name], "markLine": { "data": [{ "type": "average", "name": "平均值" }] } });
        if (item.name == "Harmony")
          console.log('fuck', scores[item.name]);
      }
    }
  }

  for (let t of tableData)
    if (t.data.length != conts.length) {
      t.data.push(0);
    }
}

let arr = fs.readdirSync('./contests');

for (let i of arr) {
  console.log(i.split('.')[0])
  load(i.split('.')[0]);
}

fs.writeFileSync("stat.json", JSON.stringify({
  teams: Array.from(teams),
  conts: conts,
  data: tableData,
  scores: scores,
  teamStats: teamStats
}));
