const fs = require('fs');

let arr = fs.readdirSync('./contests');

const spring_contests = ['vj6', 'vj8', 'vj9', 'vj10', 'vj11', 'vj12'];
const summer_contests = [/*'hd1', */'hd2', 'hd3', 'hd4', 'hd5', 'hd6', 'hd7', 'hd8', 'hd9', 'hd10', /*'nc1', 'nc2', */'nc3', 'nc4', 'nc5', 'nc6', 'nc7', 'nc8', 'nc9', 'nc10']

function load_contests(contests, belong_name) {
    let teams = new Set(),
        conts = [],
        tableData = [],
        scores = {};

    let teamStats = {};

    function load(contest) {
        teamStats[contest] = {};
        conts.push(contest);
        let data = JSON.parse(fs.readFileSync(`../data/contests/${contest}.json`));
        let probCount = 0;
        let acc = {}
        let maxSolved = 0;
        let teamsCount = 0;
        while (String.fromCharCode(probCount + 'A'.charCodeAt(0)) in data[0].detail) {
            acc[String.fromCharCode(probCount + 'A'.charCodeAt(0))] = 0;
            probCount++;
        }

        for (let item of data) {
            let solved = 0;
            for (let prob in item.detail) {
                if (item.detail[prob].time != -1)
                    acc[prob] += 1;
                solved += 1;
            }
            maxSolved = Math.max(maxSolved, solved);
            if (solved > 0)
                teamsCount += 1;
        }

        // let cnt200 = 0;
        // 
        // for (let i in data) {
        //   if (i == "200")
        //     break;
        // 
        //   let item = data[i];
        //   for (let prob in item.detail) {
        //     if (item.detail[prob].time != -1)
        //       cnt200 += 1;
        //   }
        // }

        const teamsNumber = {
            "vj6": 82,
            "vj8": 42,
            "vj9": 244,
            "vj10": 250,
            "vj11": 183,
            "vj12": 198,
        }

        if (contest.indexOf("vj") != -1) {
            teamsCount = teamsNumber[contest];
        }

        console.log(contest, maxSolved, teamsCount);

        const buptHDU = {
            "team304": "摩可彭塔斯（区庆亮，鲍睿钊，谭怡萱）",
            "team303": "网瘾犯了求求你把牌子给我（刘益铭，陈杰祥，谢志宏）",
            "team302": "彰显王威吧，踏遍世间的十二辉剑！（张颢龄，谢牧航，王若竹）",
            "team310": "遥遥领先于友队（王昰妍，梁浩然，李鹏烁）",
            "team307": "好好想想（司睿洋，尹昱钦，张泽文）",
            "team313": "堂吉诃德（卢安来，王冀恒，管庆涵）",
            "team309": "帮帮我，评测机老爷爷！（田苗，曾巍，蔡禹煊）",
            "team306": "[AI]GPT4o（袁桦斌，杨毅霖，马骐荣）",
            "team312": "如果爆零能报销回家车费吗（赵佳一，陈育堃，李天阳）",
            "team305": "试者如斯夫，不舍昼夜（安澍，秦维斌，李泽林）",
            "team308": "世界其实是一个巨大的华为手机（赵瑞霖，李乐扬，张智成）",
            "team301": "嘉然今天吃汉堡（王智炜，胡诚成，李博识）",
            "team413": "我宣布以上成绩无效（田艺彬，王华德，李子俊）",
            "team314": "歪日，这么虾头？（安奕轩，谢楠，林米乐）",
            "team319": "金牌厨师（乔函祺，李思远，马铂凯）",
            "team315": "DP_PTSD（王垚烨，蒙忠格，黄志阳）",
            "team316": "吃堡没吃饱（吴优，单一凡，金旭一）",
            "team318": "我太想AC了（马云霄，侯尔为，刘奕安）",
            "team317": "4000g_Pt（冯国晟，于洋，马廷良）",
            "team311": "对了没？如队（曾行周，钱文韬，徐衍巅）",
        }
        const buptNC = {
            "team304": "Mocopentas",
            "team303": "网瘾犯了求求你把牌子给我",
            "team302": "彰显王威吧，踏遍世间的十二辉剑",
            "team310": "遥遥领先于友队",
            "team307": "好好想想_",
            "team313": "Don_Quixote",
            "team309": "帮帮我，测评机老爷爷！",
            "team306": "[AI]GPT4o",
            "team312": "如果爆零能报销回家车费吗",
            "team305": "逝者如斯夫不舍昼夜",
            "team308": "世界其实是一个巨大的华为手机",
            "team301": "嘉然今天吃汉堡",
            "team413": "我宣布以上成绩无效",
            "team314": "歪日，这么虾头？",
            "team319": "金牌厨师",
            "team315": "DP_PTSD",
            "team316": "Humgry",
            "team318": "我太想AC了",
            "team317": "4000g_PT",
            "team311": "对了没？如队",
        }
        const buptVJ = {
            "team304": "mocopentas",
            "team303": "pair_Ac_Ac",
            "team302": "Joyeuse_Ordre",
            "team310": "Liangsheng298",
            "team307": "_nepenthe_",
            "team313": "Don_Quixote",
            "team309": "zengwei1",
            "team306": "three_newbie",
            "team312": "yidau",
            "team305": "neetman",
            "team308": "nzot",
            "team301": "UltraCat",
            "team413": "err_Grade",
            "team314": "Bush_Gamma",
            "team319": "O_start",
            "team315": "DP_PTSD",
            "team316": "Humgry",
            "team318": "WeMissAcSoMuch",
            "team317": "4000g_Pt",
            "team311": "void_WarmUp",
        }
        let hi = -1;
        for (let i in data) {
            let item = data[i];
            let rank = parseInt(item.rank);
            let cnt = 0;
            for (let prob in item.detail) {
                if (item.detail[prob].time != -1)
                    cnt += 1;
            }
            let score = Math.max(0, cnt * (500 - parseInt(item.rank)));
            if (hi == -1)
                hi = score;
            score = score / hi * 100;

            if (contest.indexOf("vj") != -1) {
                score = Math.max(0, 100 * cnt / maxSolved * ((teamsCount - rank + 1) / teamsCount)); // 2024 春季训练计分方式
            }

            if (contest.indexOf("hd") != -1) {
                item.school = (item.name.split('   '))[1];
                item.name = (item.name.split('   '))[0];
                if (item.name in buptHDU)
                    item.name = buptHDU[item.name];
            }

            if (contest.indexOf("cc") != -1) {
                item.school = (item.name.split(' '))[2];
                item.name = (item.name.split(' '))[1];
            }

            if (contest.indexOf("ic") != -1) {
                item.school = (item.name.split(' '))[0];
                item.name = (item.name.split(' '))[1];
            }

            if (contest.indexOf("vj") != -1) {
                item.school = "北京邮电大学";
                item.name = (item.name.split('('))[0];
            }

            let HDUname = "";
            if (Object.values(buptHDU).includes(item.name) && item.school == "北京邮电大学") {
                HDUname = item.name;
            }
            else if (Object.values(buptNC).includes(item.name) && item.school == "北京邮电大学") {
                for (let key in buptNC) {
                    if (buptNC[key] == item.name) {
                        HDUname = buptHDU[key];
                    }
                }
            }
            else if (Object.values(buptVJ).includes(item.name)) {
                item.school = "北京邮电大学";
                for (let key in buptVJ) {
                    if (buptVJ[key] == item.name) {
                        HDUname = buptHDU[key];
                    }
                }
            }

            if (HDUname == "") {
                continue;
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

        for (let t of tableData)
            if (t.data.length != conts.length) {
                t.data.push(0);
            }
    }

    for (let i of arr) {
        contest_name = i.split('.')[0];
        if (contests.includes(contest_name)) {
            load(contest_name);
            console.log(`${belong_name} contest `, i.split('.')[0], " generated.")
        }
    }

    fs.writeFileSync(`data/${belong_name}_stat.json`, JSON.stringify({
        teams: Array.from(teams),
        conts: conts,
        data: tableData,
        scores: scores,
        teamStats: teamStats
    }));
}

load_contests(spring_contests, 'spring');
load_contests(summer_contests, 'summer');