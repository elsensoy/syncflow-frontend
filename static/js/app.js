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

    // Websocket connection for audio streaming
    var ws = new WebSocket("ws://localhost:8765/");  // Adjust port as needed

    processor.onaudioprocess = function(e) {
        var left = e.inputBuffer.getChannelData(0);
        var convertedData = convertFloat32ToInt16(left);
        ws.send(convertedData);
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

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess)
    .catch(handleError);

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

socket.on('update_transcript', function(data) {
    document.getElementById('transcript').textContent = data.transcript;
});