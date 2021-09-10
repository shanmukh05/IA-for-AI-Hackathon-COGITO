window.onload = function() {
  
    var file = document.getElementById("thefile");
    var audio = document.getElementById("audio");
    
    file.onchange = function() {
      var files = this.files;
      audio.src = URL.createObjectURL(files[0]);
      audio.load();
      audio.play();
      var context = new AudioContext();
      var src = context.createMediaElementSource(audio);
      var analyser = context.createAnalyser();
  
      var canvas = document.getElementById("canvas");
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      var ctx = canvas.getContext("2d");
  
      src.connect(analyser);
      analyser.connect(context.destination);
  
      analyser.fftSize = 256;
  
      var bufferLength = analyser.frequencyBinCount;
      console.log(bufferLength);
  
      var dataArray = new Uint8Array(bufferLength);
  
      var WIDTH = canvas.width;
      var HEIGHT = canvas.height;
  
      var barWidth = (WIDTH / bufferLength) * 2.5;
      var barHeight;
      var x = 0;
  
      function renderFrame() {
        requestAnimationFrame(renderFrame);
  
        x = 0;
  
        analyser.getByteFrequencyData(dataArray);
  
        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
  
        for (var i = 0; i < bufferLength; i++) {
          barHeight = dataArray[i];
          
          var r = barHeight + (25 * (i/bufferLength));
          var g = 250 * (i/bufferLength);
          var b = 50;
  
          ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
          ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
  
          x += barWidth + 1;
        }
      }
  
      audio.play();
      renderFrame();
    };
  };


$('#btn-predict').click(function () {
    var result = document.getElementById("label");	 
    var probs = document.getElementById("probs");
    var audio_data = new FormData($('#upload-file')[0]);
    $.ajax({
        type: 'POST',
        url: '/predict',
        data: audio_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function (data) {
            var url = "url('/static/images/".concat(data["pred"],".png')");
            result.style.backgroundImage = url ;
            
            if(data["prob"] != undefined){
              probs.style.backgroundImage = "url('/static/images/probs_final.png')";
              $('#proba_display_0').text(data["prob"][0]);
              $('#proba_display_1').text(data["prob"][1]);
              $('#proba_display_2').text(data["prob"][2]);
              $('#proba_display_3').text(data["prob"][3]);
              $('#proba_display_4').text(data["prob"][4]);
              $('#proba_display_5').text(data["prob"][5]);
              $('#proba_display_6').text(data["prob"][6]);
            }
            console.log(data["prob"]);
        },
    });
});