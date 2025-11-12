// Elements
const userIdInput = document.getElementById('userid-input');
const taskNameInput = document.getElementById('taskname-input');
const fetchHistoryBtn = document.getElementById('fetch-history-btn');
const deleteHistoryBtn = document.getElementById('delete-history-btn');
const refreshBtn = document.getElementById('refresh-btn');
const historyList = document.getElementById('hlist');
const chatContainer = document.getElementById('chat-container');
const promptInput = document.getElementById('prompt-input');
const generateBtn = document.getElementById('generate-button');

let chatMessages = [];
let lastHistoryData = [];
let lastUserId = null;
let lastTaskName = null;
let lastMode = "user"; // or "task"
let activeHistoryIndex = null;

let observer;
let ignoreHighlight = false;

// Enable generate button only if userId, taskName and prompt input are non-empty
function updateGenerateButtonState() {
  generateBtn.disabled = !(
    userIdInput.value.trim() &&
    taskNameInput.value.trim() &&
    promptInput.value.trim()
  );
}
userIdInput.addEventListener('input', updateGenerateButtonState);
taskNameInput.addEventListener('input', updateGenerateButtonState);
promptInput.addEventListener('input', updateGenerateButtonState);

// Render chat messages
function renderChat() {
  if (chatMessages.length === 0) {
    chatContainer.innerHTML = '<div style="color:#7daaff; text-align:center; margin-top:20vh; font-size:1rem;">Start your conversation...</div>';
    return;
  }
  chatContainer.innerHTML = '';
  chatMessages.forEach(({role, content, code}, idx) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg ' + (role === 'user' ? 'user' : 'bot');
    msgDiv.textContent = content;
    msgDiv.dataset.histIdx = idx;
    chatContainer.appendChild(msgDiv);
    if (code) {
      const pre = document.createElement('pre');
      pre.className = 'code-block';
      pre.textContent = code;
      pre.dataset.histIdx = idx;
      chatContainer.appendChild(pre);
    }
  });
  chatContainer.scrollTop = chatContainer.scrollHeight;
  setupScrollSync();
}

// Render history (reverse for chronological order)
function renderHistoryList(histories) {
  historyList.innerHTML = '';
  if (!histories.length) {
    const li = document.createElement('li');
    li.textContent = 'No history found.';
    li.style.color = '#7399c9';
    li.style.fontStyle = 'italic';
    historyList.appendChild(li);
    return;
  }
  histories.slice().reverse().forEach((entry, idx) => {
    const li = document.createElement('li');
    li.tabIndex = 0;
    if (idx === activeHistoryIndex) li.classList.add('active');

    const contentDiv = document.createElement('div');
    contentDiv.className = 'history-content';
    contentDiv.title = `Prompt: ${entry.prompt}\nResponse: ${entry.message}`;

    const promptDiv = document.createElement('div');
    promptDiv.className = 'hitem-prompt';
    promptDiv.textContent = entry.prompt;
    contentDiv.appendChild(promptDiv);

    const responseDiv = document.createElement('div');
    responseDiv.className = 'hitem-response';
    responseDiv.textContent = entry.message;
    contentDiv.appendChild(responseDiv);
    li.appendChild(contentDiv);

    // Delete button
    const delBtn = document.createElement('button');
    delBtn.className = 'delete-history-btn';
    delBtn.title = 'Delete this history entry';
    delBtn.type = 'button';
    delBtn.innerHTML = '🗑';
    delBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (!confirm('Are you sure you want to delete this history entry?')) return;
      try {
        const user_id = userIdInput.value.trim();
        const task_name = entry.task_name || taskNameInput.value.trim();
        const prompt_text = entry.prompt;
        if (!user_id || !task_name || !prompt_text) {
          alert('Cannot delete: Missing info.');
          return;
        }
        const params = new URLSearchParams({ user_id, task_name, prompt: prompt_text });
        const res = await fetch(`/history/entry?${params.toString()}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Failed to delete entry.');
        const data = await res.json();
        alert(data.message || 'Entry deleted.');
        await fetchHistory();
      } catch (err) {
        alert('Delete failed: ' + err.message);
      }
    });
    li.appendChild(delBtn);

    // On click: load conversation up to this history
    li.addEventListener('click', () => {
      activeHistoryIndex = idx;
      loadHistoryEntryByIndex(idx);
      renderHistoryList(histories);
    });

    historyList.appendChild(li);
  });
}

// Load conversation up to a selected history index
function loadHistoryEntryByIndex(selectedIdx) {
  chatMessages = [];
  const ordered = lastHistoryData.slice().reverse(); 
  for (let i = 0; i <= selectedIdx; i++) {
    const entry = ordered[i];
    if (entry && entry.prompt) chatMessages.push({role: 'user', content: entry.prompt});
    if (entry && (entry.message || entry.code)) {
      let resp = entry.message || '';
      let code = entry.code || '';
      if (code && resp.includes(code)) resp = resp.replace(code, '').trim();
      chatMessages.push({role: 'bot', content: resp, code});
    }
  }
  renderChat();
  promptInput.value = '';
  promptInput.focus();
}

// Scroll sync
function setupScrollSync() {
  if(observer){ observer.disconnect(); }
  const chatMsgs = chatContainer.querySelectorAll('.chat-msg');
  if(chatMsgs.length === 0){ return; }
  observer = new IntersectionObserver((entries) => {
    if(ignoreHighlight) return;
    let maxRatio = 0;
    let inViewIdx = 0;
    entries.forEach(entry => {
      if(entry.isIntersecting && entry.intersectionRatio > maxRatio) {
        maxRatio = entry.intersectionRatio;
        inViewIdx = Number(entry.target.dataset.histIdx);
      }
    });
    highlightLeftForChat(Math.floor(inViewIdx / 2));
  }, { root: chatContainer, threshold: [0.5] });
  chatMsgs.forEach(msg => observer.observe(msg));
}

// Highlight active history
function highlightLeftForChat(histIdx) {
  const leftItems = historyList.querySelectorAll('li');
  leftItems.forEach((li, idx) => {
    if(idx === histIdx) li.classList.add('active');
    else li.classList.remove('active');
  });
}

// Fetch history
async function fetchHistory() {
  const userId = userIdInput.value.trim();
  const taskName = taskNameInput.value.trim();
  if (!userId) {
    alert('User ID is required to fetch history.');
    return;
  }
  let endpoint = '/history';
  let params = { user_id: userId };
  if (taskName) { endpoint = '/history/task'; params.task_name = taskName; }
  try {
    const url = endpoint + '?' + new URLSearchParams(params);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.history)) {
      alert('Unexpected data format received');
      return;
    }
    lastHistoryData = data.history;
    lastUserId = userId;
    lastTaskName = taskName || null;
    lastMode = taskName ? 'task' : 'user';
    activeHistoryIndex = null;
    renderHistoryList(lastHistoryData);
    loadHistoryEntryByIndex(lastHistoryData.length - 1);
  }
  catch (err) { alert('Error fetching history: ' + err.message); }
}

// Delete all history
async function deleteHistory() {
  const userId = userIdInput.value.trim();
  const taskName = taskNameInput.value.trim();
  if (!userId) { alert('User ID is required to delete history.'); return; }
  let endpoint = '/history';
  let params = { user_id: userId };
  if (taskName) { endpoint = '/history/task'; params.task_name = taskName; }
  try {
    const url = endpoint + '?' + new URLSearchParams(params);
    const response = await fetch(url, { method: 'DELETE' });
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const data = await response.json();
    lastHistoryData = [];
    activeHistoryIndex = null;
    renderHistoryList([]);
    chatMessages = [];
    renderChat();
    alert(data.message || 'History deleted');
  }
  catch(err) { alert('Error deleting history: ' + err.message); }
}

// Refresh
function refreshPage() { location.reload(); }

// Generate response
async function generateResponse() {
  const userId = userIdInput.value.trim();
  const taskName = taskNameInput.value.trim();
  const promptText = promptInput.value.trim();
  if (!(userId && taskName && promptText)) {
    alert('Please fill User ID, Task Name, and prompt to generate');
    return;
  }
  chatMessages.push({ role: 'user', content: promptText });
  renderChat();
  promptInput.value = '';
  generateBtn.disabled = true;
  try {
    const res = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, task_name: taskName, prompt: promptText })
    });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    if (data.response) {
      chatMessages.push({
        role: 'bot',
        content: data.response.message || '',
        code: data.response.code || ''
      });
      renderChat();
    } else { alert('No response content'); }
  }
  catch (err) { alert('Generation failed: ' + err.message); }
  finally { generateBtn.disabled = false; }
}

fetchHistoryBtn.addEventListener('click', fetchHistory);
deleteHistoryBtn.addEventListener('click', deleteHistory);
refreshBtn.addEventListener('click', refreshPage);
generateBtn.addEventListener('click', generateResponse);
promptInput.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (!generateBtn.disabled) generateBtn.click(); } });

window.onload = () => { renderChat(); updateGenerateButtonState(); userIdInput.focus(); };
