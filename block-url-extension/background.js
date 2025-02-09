chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  chrome.storage.sync.get({ words: [] }, (data) => {
    const words = data.words;
    const url = details.url.toLowerCase();

    if (words.some(word => url.includes(word.toLowerCase()))) {
      chrome.tabs.update(details.tabId, { url: "https://google.com" }); // Redirect to this URL
    }
  });
});