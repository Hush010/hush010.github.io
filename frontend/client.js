async function startCall() {
  const pc = new RTCPeerConnection();

  // Play incoming audio
  const audio = document.createElement("audio");
  audio.autoplay = true;
  pc.ontrack = (event) => {
    audio.srcObject = event.streams[0];
  };

  // Capture microphone
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  stream.getTracks().forEach(track => pc.addTrack(track, stream));

  // Data channel (optional for debugging)
  pc.createDataChannel("chat");

  // Create offer
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  // Send offer to backend
  const res = await fetch("http://localhost:8000/offer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sdp: offer.sdp, type: offer.type }),
  });

  const answer = await res.json();
  await pc.setRemoteDescription(answer);
}

document.getElementById("start").onclick = startCall;
