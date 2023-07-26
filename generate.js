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
	let Acc2Hours = {}
  while (String.fromCharCode(probCount + 'A'.charCodeAt(0)) in data[0].detail) {
    acc[String.fromCharCode(probCount + 'A'.charCodeAt(0))] = 0;
    probCount++;
  }
	console.log("总题数:",probCount);
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

	let Max2Hours = -1;

	for (let i in data) {
		let item = data[i];
		Acc2Hours[i] = 0;
		for (let prob in item.detail) {
			if(item.detail[prob].time <= 120 && item.detail[prob].time != -1)
				Acc2Hours[i] += 1;
		}
		Max2Hours = Math.max(Max2Hours,Acc2Hours[i]);
	}

	console.log("2小时过题最多数：",Max2Hours);
  const buptHDU = {
    "team401": "打完去超市买点东西吃",
    "team402": "三个菜鸟",
    "team403": "野鸡大队",
    "team404": "来了去了",
    "team405": "鹰之一手",
    "team406": "未闻队名",
    "team407": "奥特猫",
    "team408": "最佳柴郡",
    "team409": "逆转结局",
    "team410": "字节御宅族",
    "team411": "你们队得过什么奖",
    "team412": "默认用户名",
    "team413": "啊对对队",
    "team414": "左右魔性穿梭",
    "team415": "再做一道就开摆",
    "team416": "六目相对",
    "team417": "我有起名困难症",
    "team418": "你说的队",
    "team419": "三只蒟蒻",
    "team1051": "未命名-1",
  }
  buptNC = {
    "team401": "打完去超市买点东西吃",
    "team402": "三个菜鸟_",
    "team403": "野鸡大队",
    "team404": "来了去了",
    "team405": "OneHandofWarhawks",
    "team406": "Unnamed Team",
    "team407": "UltraCat",
    "team408": "最佳柴郡",
    "team409": "ReverseEnding",
    "team410": "字节御宅族ByteOtakus",
    "team411": "你们队得过什么奖",
    "team412": "默认用户名",
    "team413": "Ah对对对队",
    "team414": "左右魔性穿梭队",
    "team415": "再做一道就开摆",
    "team416": "六目相对",
    "team417": "我有起名困难症",
    "team418": "BUPT-你说的队",
    "team419": "三只蒟蒻_threekonjaks",
    "team1051": "未命名-1",
  }
  let hi = -1;

	for (let i in data) {
		let item = data[i];
		let cnt = 0;
		for (let prob in item.detail) {
			if (item.detail[prob].time != -1)
				cnt += 1;
		}
		if(cnt >= Max2Hours) 
			hi = Math.max(0, cnt / cnt200 * (500 - parseInt(item.rank)));
	}
	console.log("标准分:",hi)
  for (let i in data) {
    let item = data[i];
    let cnt = 0;
    for (let prob in item.detail) {
      if (item.detail[prob].time != -1)
        cnt += 1;
    }
    let score = Math.max(0, cnt / cnt200 * (500 - parseInt(item.rank)));
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
    else if (Object.values(buptNC).includes(item.name)) {
      // Find the item.name in buptHDU which is the same team
      let HDUname = "";
      for (let key in buptNC) {
        if (buptNC[key] == item.name) {
          HDUname = buptHDU[key];
        }
      }
      teams.add(HDUname);
      teamStats[contest][HDUname] = `${item.rank}/${cnt}/${score.toFixed(2)}`;
      let found = false;
      for (let t of tableData)
        if (t.name == HDUname) {
          found = true;
          scores[HDUname].push(parseFloat(score.toFixed(2)));
        }
      if (!found) {
        scores[HDUname] = [];
        for (let i = 0; i < conts.length - 1; ++i)
          scores[HDUname].push(0);
        scores[HDUname].push(parseFloat(score.toFixed(2)));
        tableData.push({ "name": HDUname, "type": "line", "data": scores[HDUname], "markLine": { "data": [{ "type": "average", "name": "平均值" }] } });
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
