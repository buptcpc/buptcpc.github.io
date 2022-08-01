const axios = require('axios');
const fs = require('fs')

let all = [], ALL = 31, cid = 33190

function work(cid) {
  let ranks = {}, i = 0
  while (i < ALL) {
    console.log(i)
    axios.get(`https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id=${cid}&page=${i + 1}&limit=0&_=1626692170101`).then(res => {
      // 将页面数据转为$对象
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
    });
    i += 1
  }

  setTimeout(() => {
    let arr = []
    for (let i in ranks) {
      arr.push(ranks[i])
    }
    fs.writeFile(`./${cid}.json`, JSON.stringify(arr), err => {
      if (err) {
        console.error(err)
        return
      }
    })
  }, 5000)
}


work(cid)

