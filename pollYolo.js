const request = require('request');

URL = "http://192.168.16.39:5000/detect.json";
var N = 0;

function checkYolo(url) {
    N += 1;
    var url2 = url+"?N="+N;
    console.log("Getting yolo info from", url2);
    request(url2, { json: true }, (err, res, yoloRes) => {
        if (err) {
            console.log("Error", err);
            return console.log(err);
        }
        //console.log(yoloRes);
        var ut = yoloRes.unixtime;
        console.log("ut", ut);
        var objs = yoloRes.objects;
        objs.forEach(obj => {
            //console.log(obj);
            console.log("label", obj.label)
        });
        console.log("");
        checkYolo(url);
    });
}

checkYolo(URL)



