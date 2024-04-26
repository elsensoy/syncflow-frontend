//app.js
var socket = io();

var audioContext = new (window.AudioContext || window.webkitAudioContext)();
var microphone;
var input;
var processor;

function handleSuccess(stream) {
    microphone = stream;
    input = audioContext.createMediaStreamSource(stream);
    processor = audioContext.createScriptProcessor(1024, 1, 1);

    input.connect(processor);
    processor.connect(audioContext.destination);

    processor.onaudioprocess = function(e) {
        var left = e.inputBuffer.getChannelData(0);
        // Convert Float32Array to something you can send over
        var convertedData = convertFloat32ToInt16(left);
        socket.emit('audio_data', convertedData);
    };
}

function handleError(error) {
    console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
    alert('Error accessing audio devices. Please check microphone permissions.');
}

function convertFloat32ToInt16(buffer) {
    var l = buffer.length;
    var buf = new Int16Array(l);
    while (l--) {
        buf[l] = Math.min(1, buffer[l]) * 0x7FFF;
    }
    return buf.buffer;
}

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess)
    .catch(handleError);

function startRecording() {
    if (!microphone) {
        alert('Microphone is not accessible. Please reload and allow microphone access.');
        return;
    }
    socket.emit('start_recording');
    document.getElementById('live-indicator').textContent = 'Recording...';
}

function stopRecording() {
    if (processor && microphone) {
        processor.disconnect();
        microphone.getTracks().forEach(track => track.stop());
    }
    socket.emit('stop_recording');
    document.getElementById('live-indicator').textContent = 'Stopped';
}

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
    document.getElementById('live-indicator').textContent = 'Disconnected';
});

socket.on('reconnect', function() {
    console.log('Reconnected to server');
    document.getElementById('live-indicator').textContent = 'Reconnected - Ready to record';
});

socket.on('transcript_update', function(data) {
    document.getElementById('transcript').textContent = data.transcript;
});

