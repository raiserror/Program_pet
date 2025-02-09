chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  chrome.storage.sync.get({ words: [] }, (data) => {
    const words = data.words;
    const url = decodeURIComponent(details.url).toLocaleLowerCase(); 

    if (words.some(word => url.includes(word.toLocaleLowerCase()))) {
      chrome.tabs.update(details.tabId, { url: "https://google.com" });
    }
  });
});