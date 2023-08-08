const axios = require('axios');
const fs = require('fs')
const config = require("./config.json")

let all = [], ALL = 18

async function work(cid, index) {
  let ranks = {}, i = 0
  while (i < ALL) {
    const res = await axios.get(`https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id=${cid}&page=${i + 1}&limit=0&_=1626692170101`);
    for (let o of res.data.data.rankData) {
      let d = {}
      for (let i = 0; i < res.data.data.problemData.length; ++i) {
        d[res.data.data.problemData[i].name] = {
          time: o.scoreList[i].acceptedTime == -1 ? o.scoreList[i].acceptedTime : Math.floor((o.scoreList[i].acceptedTime - res.data.data.basicInfo.contestBeginTime) / 1000 / 60),
          tries: o.scoreList[i].failedCount
        }
      }
      ranks[o.ranking] = {
        detail: d,
        name: o.userName,
        school: o.school,
        rank: o.ranking
      }
    }
    i += 1
  }

  let arr = []
  for (let i in ranks) {
    arr.push(ranks[i])
  }
  if (arr.length == 0) {
    console.log(`nowcoder contest ${cid} is not over.`)
    return
  }
  fs.writeFileSync(`contests/nc${index + 1}.json`, JSON.stringify(arr), err => {
    if (err) {
      console.error(err)
    }
  })
  console.log(`nowcoder contest ${cid} exported.`)
}


function search_contests(keyword) {
  const url =  `https://ac.nowcoder.com/acm-heavy/acm/contest/search-detail?searchName=${encodeURIComponent(keyword)}&topCategoryFilter=13`
  axios.get(url).then(async res => {
    // <a href="/acm/contest/57362" target="_blank">57362</a>
    const regexp = /<a href="\/acm\/contest\/(\d+?)" target="_blank">(\d+?)<\/a>/g
    await Promise.allSettled(Array.from(res.data.matchAll(regexp)).map(i => i[1]).sort((a, b) => a - b).map((i, index) => work(i, index)))
  })
}

// work(cid)

search_contests("2023牛客暑期多校训练营")
