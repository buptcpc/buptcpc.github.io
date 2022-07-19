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
    "team201": "热爱106种算法的你",
    "team202": "TO_BE_CONTINUE_",
    "team203": "三只蒟蒻_threekonjaks",
    "team204": "沙河摸鱼队",
    "team205": "野鸡大队",
    "team206": "罚时大队",
    "team207": "Not_responding",
    "team208": "一起开车",
    "team209": "intmian()",
    "team210": "MeUmy天下第一",
    "team211": "六目相对",
    "team212": "珊瑚宫心海",
    "team213": "Triple",
    "team214": "NoBraceNewline",
    "team215": "膜你退火",
    "team216": "Against_the_odds",
    "team217": "callq_AC",
    "team218": "Luna_2235",
    "team219": "仙贝",
    "team220": "三个诸葛亮不如臭裨将",
    "team221": "REPET_AC",
    "team222": "void_WarmUp"
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
    if (contest.indexOf("hd") != -1) {
      item.school = (item.name.split('   '))[1];
      item.name = (item.name.split('   '))[0];
      if (item.name in buptHDU)
        item.name = buptHDU[item.name];
    }

    if (contest.indexOf("cc") != -1) {
      item.school = (item.name.split(' '))[2];
      item.name = (item.name.split(' '))[1];
      //if (item.name in buptHDU)
      //  item.name = buptHDU[item.name];
    }

    if (contest.indexOf("ic") != -1) {
      item.school = (item.name.split(' '))[0];
      item.name = (item.name.split(' '))[1];
      //if (item.name in buptHDU)
      //  item.name = buptHDU[item.name];
    }

    if (Object.values(buptHDU).includes(item.name)) {
      teams.add(item.name);
      teamStats[contest][item.name] = `${item.rank}/${cnt}/${score.toFixed(2)}`;
      let found = false;
      for (let t of tableData)
        if (t.name == item.name) {
          found = true;
          scores[item.name].push(parseFloat(score.toFixed(2)));
        }
      if (!found) {
        scores[item.name] = [];
        for (let i = 0; i < conts.length - 1; ++i)
          scores[item.name].push(0);
        scores[item.name].push(parseFloat(score.toFixed(2)));
        tableData.push({ "name": item.name, "type": "line", "data": scores[item.name], "markLine": { "data": [{ "type": "average", "name": "平均值" }] } });
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
