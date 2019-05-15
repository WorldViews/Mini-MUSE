
console.log("Loading MUSEControl.js");

var CURRENT_CHOICE = null;
var CURRENT_YAW = 0;

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

if (typeof io == "undefined") {
    var io = require("socket.io-client");
}

class MUSEControl
{
    constructor(sioURL) {
        var inst = this;
        if (!sioURL) {
            //var sioURL = "http://platonia:4000";
            sioURL = document.location.host;
            var serverName = getParameterByName("server");
            if (serverName) {
                sioURL = "http://"+serverName+":4000";
            }
        }
        this.url = sioURL;
        console.log("getting socket at: "+sioURL);
        this.sock = io(sioURL);
        console.log("Got socket "+this.sock);
        this.sock.on("pano", msg => {
            inst.handleMessage(msg);
        });
        //setInterval(function() { inst.update(); }, 50);
    }

    handleMessage(msg) {
        console.log("Got message: ", msg);
    }

    getURL() { return this.url; }

    sendMessage(msg, channel) {
        channel = channel || "MUSE";
        var jstr = JSON.stringify(msg);
        console.log("MUSEControl.sendMessage "+channel+" "+ jstr);
        this.sock.emit(channel, jstr);
    }

    setYawPitch(yaw, pitch)
    {
        pitch = pitch || 0;
        let msg = {'type': 'pano.control', panoView: [yaw, pitch]};
        console.log("setYawPitch sending "+JSON.stringify(msg));
        portal.sendMessage(msg);
    }

    panScene(deg)
    {
        //deg = deg || 0.5;
        deg = deg || 1.0;
        CURRENT_YAW += deg;
        console.log("pan scene by "+deg);
        portal.sendMessage({'type': 'pano.control',
                            panoView: [CURRENT_YAW,0]} );
    }
    
    setPlayTime(t) {
        //portal.sendMessage({'type': 'pano.control', time: t} );
        this.sendMessage({'type': 'pano.control', time: t} );
    }

    play() {
        this.sendMessage({type: 'pano.control', playSpeed: 1} );
    }

    pause() {
        this.sendMessage({type: 'pano.control', playSpeed: 0} );
    }

    setVolume(v) {
        this.sendMessage({type: 'pano.control', volume: v} );
    }

    setVideo(videoId) {
        console.log("MUSEControl.setVideo "+videoId);
        var msg = {type: 'MUSE.control',
                   videoId: videoId
                  };
        this.sendMessage(msg);
    }
}

function getJSON(url, handler)
{
    console.log("Util.getJSON: "+url);
    $.ajax({
        url: url,
        dataType: 'text',
        success: function(str) {
            var data;
            try {
                data = JSON.parse(str);
            }
            catch (err) {
                console.log("err: "+err);
                alert("Error in json for: "+url+"\n"+err);
                return;
            }
            handler(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            reportError("Failed to get JSON for "+url);
        }
    });
}

if (typeof exports !== 'undefined') {
    console.log("setting up exports");
    exports.MUSEControl = MUSEControl;
}
