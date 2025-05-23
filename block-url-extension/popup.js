document.getElementById('addWord').addEventListener('click', () => {
  const word = document.getElementById('wordInput').value.trim().toLocaleLowerCase();
  if (word) {
    chrome.storage.sync.get({ words: [] }, (data) => {
      const words = data.words;
      if (!words.includes(word)) {
        words.push(word);
        chrome.storage.sync.set({ words }, () => {
          document.getElementById('wordInput').value = '';
        });
      }
    });
  }
});

document.getElementById('manageWords').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});