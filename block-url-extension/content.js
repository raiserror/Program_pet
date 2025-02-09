const redirectUrl = "https://www.google.com"; 

chrome.storage.sync.get({ blockedWords: [] }, function(data) {
  const blockedWords = data.blockedWords;
  const pageText = document.body.innerText.toLowerCase();

  const shouldBlock = blockedWords.some(word => pageText.includes(word.toLowerCase()));

  if (shouldBlock) {
    window.location.href = redirectUrl;
  }
});