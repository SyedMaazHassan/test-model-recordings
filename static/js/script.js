window.addEventListener('DOMContentLoaded', () => {
    const getMic = document.getElementById('mic');
    const recordButton = document.getElementById('record');
    const list = document.getElementById('recordings');
    if ('MediaRecorder' in window) {
      getMic.addEventListener('click', async () => {
        getMic.setAttribute('hidden', 'hidden');
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: false
          });
          const mimeType = 'audio/mp3';
          let chunks = [];
          const recorder = new MediaRecorder(stream, { type: 'audio/mp3' });
          recorder.addEventListener('dataavailable', event => {
            if (typeof event.data === 'undefined') return;
            if (event.data.size === 0) return;
            chunks.push(event.data);
          });
          recorder.addEventListener('stop', () => {
            const recording = new Blob(chunks, {
              'type' : 'audio/mp3; codecs=opus'
            });
            renderRecording(recording, list);
            startNext();
            chunks = [];
          });
          recordButton.removeAttribute('hidden');
          recordButton.addEventListener('click', () => {
            if (recorder.state === 'inactive') {
              recorder.start();
              $("#spinners-loading").css("display", "");
              recordButton.innerText = 'Stop and see next sentence';
            } else {
              recorder.stop();
              $("#spinners-loading").css("display", "none");
              recordButton.innerText = 'Start recording';
            }
          });
        } catch {
          renderError(
            'You denied access to the microphone so this demo will not work.'
          );
        }
      });
    } else {
      renderError(
        "Sorry, your browser doesn't support the MediaRecorder API, so this demo will not work."
      );
    }
  });

  var count = 0;

  function renderError(message) {
    const main = document.querySelector('main');
    main.innerHTML = `<div class="error"><p>${message}</p></div>`;
  }

  function uploadAudioBlobs(FILE) {
    console.log(FILE);
    
  }

  function renderRecording(blob, list) {
    const blobUrl = URL.createObjectURL(blob);
    const li = document.createElement('li');
    const audio = document.createElement('audio');
    const anchor = document.createElement('a');
    anchor.setAttribute('href', blobUrl);
    const now = new Date();
    anchor.setAttribute(
      'download',
      `recording-${now.getFullYear()}-${(now.getMonth() + 1)
        .toString()
        .padStart(2, '0')}-${now
        .getDay()
        .toString()
        .padStart(2, '0')}--${now
        .getHours()
        .toString()
        .padStart(2, '0')}-${now
        .getMinutes()
        .toString()
        .padStart(2, '0')}-${now
        .getSeconds()
        .toString()
        .padStart(2, '0')}.mp3`
    );
    anchor.innerText = 'Download';
    audio.setAttribute('src', blobUrl);
    audio.setAttribute('controls', 'controls');
    li.appendChild(audio);
    li.appendChild(anchor);
    list.appendChild(li);

    count += 1;

    //Now convert the blob to a mp3 file or whatever the type you want
    var mp3filefromblob = new File([blob], 'filename.mp3');

    console.log(document.getElementById("abc").files);

    document.getElementById("abc").files[0] = mp3filefromblob;

    console.log(document.getElementById("abc").files);

    $("#all-recordings").append(`


        <div class="col-sm-6 py-2">
            <div class="card">
                <div class="card-body shadow">
                    <p title="${all_selected_sentences[current]}" data-toggle="tooltip">${wrapped_text(all_selected_sentences[current], 43)}</p>

                    <audio style="width: 100%;" controls>
                    <source src="${blobUrl}" type="audio/mpeg">
                    Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
        </div>
    
    
    `);

    // <p title="${all_selected_sentences[current]}" data-toggle="tooltip">${wrapped_text(all_selected_sentences[current], 23)}</p>




    console.log(mp3filefromblob);
    let stringing = JSON.stringify(mp3filefromblob);
    console.log(stringing);
    var formData = new FormData();
    formData.append('audio', mp3filefromblob);
    formData.append('maaz', JSON.stringify({name: "maaz"}));
    
    $.ajax({
        url: "{% url 'abc2' %}",
        type: "GET",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        success: (response)=>{
          console.log(response);
          console.log("Asdsadas");
        }
    });


    
    var file = {};
    var xhr = new XMLHttpRequest();
    xhr.open('GET', blobUrl, true);
    xhr.responseType = 'blob';
    xhr.onload = function(e) {
        if (this.status == 200) {
            file.file = this.response;
            file.name = "whatever_filename.mp3";
            // file.size = getYourBlobSize();
            file.size = blob.size
            file.type = "audio/mp3";
            uploadAudioBlobs(file);
        }
    };
    xhr.send();
    
    
    console.log(file);
    
    //on rec.stop() 
    console.log(blob);
    // var xhttp = new XMLHttpRequest();
    // xhttp.open("GET", "abc", true);
    
    // xhttp.send(data);
    // xhttp.onreadystatechange = function() {
    //     if (this.readyState == 4 && this.status == 200) {
    //         console.log(this.responseText);     
    //      }
    // };
        
    
  }