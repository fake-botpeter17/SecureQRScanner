const input = document.getElementById('qrInput');
const resetBtn = document.getElementById('resetBtn');
const qrPreview = document.getElementById('qrPreview');
const qrImage = document.getElementById('qrImage');
const statusMsg = document.getElementById('statusMsg');
const results = document.getElementById('results');

// Fake AI safety scanner
function analyzeURLSafety(url) {
  const phishingWords = ['login', 'verify', 'update', 'secure'];
  const domain = new URL(url).hostname;
  const isPhishy = phishingWords.some(w => url.toLowerCase().includes(w));
  return {
    risk: isPhishy ? 'High' : 'Low',
    reason: isPhishy ? 'Suspicious keyword detected in URL.' : 'No obvious threats detected.',
    domain
  };
}

// Fake AI privacy guard
function checkPrivacyThreats(content) {
  const patterns = ['email', 'phone', 'address', 'dob', 'ssn'];
  return patterns.filter(p => content.toLowerCase().includes(p));
}

// Fake AI chatbot explanation
async function getAIExplanation(content) {
  try {
    const response = await fetch(`http://127.0.0.1:5001/scan?url=${encodeURIComponent(content)}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const explanation = await response.text();
    return explanation;
  } catch (err) {
    console.error('Fetch error:', err);
    return '⚠️ Could not fetch explanation.';
  }
}


// Fake QR image quality check
function detectFakeQR(image) {
  return new Promise(resolve => {
    const { width, height } = image;
    resolve(width < 100 || height < 100
      ? '⚠️ Low resolution – may be a fake or unreadable QR code.'
      : '✅ Image quality is acceptable.');
  });
}

input.addEventListener('change', async () => {
  const file = input.files[0];
  if (!file) return;

  results.innerHTML = '';
  statusMsg.textContent = 'Analyzing QR code...';

  const reader = new FileReader();
  reader.onload = async e => {
    const img = new Image();
    img.src = e.target.result;
    img.onload = async () => {
      qrPreview.style.display = 'block';
      qrImage.src = img.src;
      resetBtn.style.display = 'inline-block';

      const canvas = document.createElement('canvas');
      canvas.width = img.width; canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      results.innerHTML += `<p>${await detectFakeQR(img)}</p>`;
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const code = jsQR(imageData.data, canvas.width, canvas.height);

      if (code) {
        const content = code.data;
        results.innerHTML += `<p><strong>QR Content:</strong> ${content}</p>`;
        if (content.startsWith('http')) {
          const analysis = analyzeURLSafety(content);
          results.innerHTML += `
            <p><strong>Domain:</strong> ${analysis.domain}</p>
            <p><strong>Risk Level:</strong> ${analysis.risk}</p>
            <p><strong>Reason:</strong> ${analysis.reason}</p>`;
        }
        const explanation = await getAIExplanation(content);
        results.innerHTML += `<p><strong>AI Explainer:</strong> ${explanation}</p>`;
        const privacyFlags = checkPrivacyThreats(content);
        if (privacyFlags.length) {
          results.innerHTML += `<p><strong>⚠️ Privacy Alert:</strong> data fields detected: ${privacyFlags.join(', ')}</p>`;
        }
      } else {
        results.innerHTML += '<p>❌ Unable to detect QR code.</p>';
      }
      statusMsg.textContent = 'Analysis complete.';
    };
  };
  reader.readAsDataURL(file);
});

resetBtn.addEventListener('click', () => {
  input.value = '';
  qrPreview.style.display = 'none';
  resetBtn.style.display = 'none';
  results.innerHTML = '';
  statusMsg.textContent = '';
});
