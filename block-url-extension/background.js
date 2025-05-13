chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  chrome.storage.sync.get({ words: [] }, (data) => {
    const words = data.words;
    const url = decodeURIComponent(details.url).toLocaleLowerCase();

    // Remove special characters from URL. Remove - note/del line 7, line 9 cleanedUrl -> url
    const cleanedUrl = url.replace(/[^a-zа-яё0-9]/gi, '');

    if (words.some(word => cleanedUrl.includes(word.toLocaleLowerCase()))) {
      chrome.tabs.update(details.tabId, { url: "https://google.com" });
    }
  });
});