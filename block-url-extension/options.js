function renderWords() {
  chrome.storage.sync.get({ words: [] }, (data) => {
    const wordList = document.getElementById('wordList');
    wordList.innerHTML = '';
    data.words.forEach((word, index) => {
      const li = document.createElement('li');
      li.textContent = word;
      const deleteButton = document.createElement('button');
      deleteButton.textContent = 'Delete';
      deleteButton.addEventListener('click', () => {
        data.words.splice(index, 1);
        chrome.storage.sync.set({ words: data.words }, renderWords);
      });
      li.appendChild(deleteButton);
      wordList.appendChild(li);
    });
  });
}

document.getElementById('addWord').addEventListener('click', () => {
  const word = document.getElementById('wordInput').value.trim().toLocaleLowerCase(); 
  if (word) {
    chrome.storage.sync.get({ words: [] }, (data) => {
      const words = data.words;
      if (!words.includes(word)) { 
        words.push(word);
        chrome.storage.sync.set({ words }, () => {
          document.getElementById('wordInput').value = '';
          renderWords();
        });
      }
    });
  }
});

renderWords();