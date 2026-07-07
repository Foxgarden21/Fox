const defaultWorkers = ['Pracovník 1', 'Pracovník 2', 'Pracovník 3', 'Pracovník 4'];
const defaultJobs = [
    { name: '2026-06-001 Hořice', archived: false },
    { name: '2026-06-002 Lískovice 22', archived: false },
    { name: '2026-06-003 SVJ Hostinné', archived: false }
];

let workers = JSON.parse(localStorage.getItem('foxgarden_workers')) || defaultWorkers;

// Migrate old jobs array of strings to objects if necessary
let rawJobs = JSON.parse(localStorage.getItem('foxgarden_jobs')) || defaultJobs;
let jobs = rawJobs.map(j => typeof j === 'string' ? { name: j, archived: false } : j);

let attendanceLog = JSON.parse(localStorage.getItem('foxgarden_attendance_log')) || [];

const workerSelect = document.getElementById('worker');
const jobSelect = document.getElementById('job');
const workerList = document.getElementById('workerList');
const jobList = document.getElementById('jobList');
const attendanceLogList = document.getElementById('attendanceLogList');
const adminPanel = document.getElementById('adminPanel');

// Init
function renderSelects() {
    workerSelect.innerHTML = '<option value="">-- vyber --</option>';
    workers.forEach(w => {
        workerSelect.innerHTML += `<option value="${w}">${w}</option>`;
    });

    jobSelect.innerHTML = '<option value="">-- vyber --</option>';
    jobs.forEach(j => {
        if (!j.archived) {
            jobSelect.innerHTML += `<option value="${j.name}">${j.name}</option>`;
        }
    });
}

function renderAdminLists() {
    workerList.innerHTML = '';
    workers.forEach((w, index) => {
        workerList.innerHTML += `<li style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee; align-items:center;">
            ${w} <button class="delete-btn" onclick="deleteWorker(${index})">Smazat</button>
        </li>`;
    });

    jobList.innerHTML = '';
    jobs.forEach((j, index) => {
        const titleStyle = j.archived ? "text-decoration: line-through; color: #999;" : "";
        const archiveBtn = j.archived
            ? `<button onclick="toggleArchiveJob(${index})" style="padding: 4px 8px; font-size: 12px; margin-right: 5px;">Obnovit</button>`
            : `<button onclick="toggleArchiveJob(${index})" style="padding: 4px 8px; font-size: 12px; margin-right: 5px;">Archivovat</button>`;

        jobList.innerHTML += `<li style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee; align-items:center;">
            <span style="${titleStyle}">${j.name}</span>
            <div>
                ${archiveBtn}
                <button class="delete-btn" onclick="deleteJob(${index})">Smazat</button>
            </div>
        </li>`;
    });

    attendanceLogList.innerHTML = '';
    // Show only the last 20 records
    const recentLogs = attendanceLog.slice().reverse().slice(0, 20);
    recentLogs.forEach((r, displayIndex) => {
        // We need to map the visual index back to the real index in the original array
        const realIndex = attendanceLog.length - 1 - displayIndex;
        const color = r.action === 'IN' ? 'green' : 'red';
        attendanceLogList.innerHTML += `<li style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee; align-items:center;">
            <div>
                <strong>${r.worker}</strong> - ${r.job} (${r.workType})<br>
                <span style="color:${color};">${r.action}</span> v ${r.time}
            </div>
            <button class="delete-btn" onclick="deleteLog(${realIndex})">Smazat</button>
        </li>`;
    });
}

function saveToLocalStorage() {
    localStorage.setItem('foxgarden_workers', JSON.stringify(workers));
    localStorage.setItem('foxgarden_jobs', JSON.stringify(jobs));
    localStorage.setItem('foxgarden_attendance_log', JSON.stringify(attendanceLog));
    renderSelects();
    renderAdminLists();
}

function addWorker() {
    const input = document.getElementById('newWorkerInput');
    const val = input.value.trim();
    if(val) {
        workers.push(val);
        input.value = '';
        saveToLocalStorage();
    }
}

function deleteWorker(index) {
    if(confirm('Opravdu smazat pracovníka?')) {
        workers.splice(index, 1);
        saveToLocalStorage();
    }
}

function addJob() {
    const input = document.getElementById('newJobInput');
    const val = input.value.trim();
    if(val) {
        jobs.push({ name: val, archived: false });
        input.value = '';
        saveToLocalStorage();
    }
}

function deleteJob(index) {
    if(confirm('Opravdu trvale smazat zakázku?')) {
        jobs.splice(index, 1);
        saveToLocalStorage();
    }
}

function toggleArchiveJob(index) {
    jobs[index].archived = !jobs[index].archived;
    saveToLocalStorage();
}

function deleteLog(index) {
    if(confirm('Opravdu smazat tento záznam docházky?')) {
        attendanceLog.splice(index, 1);
        saveToLocalStorage();
    }
}

// Admin Auth
document.getElementById('btnAdmin').addEventListener('click', () => {
    document.getElementById('adminModal').style.display = 'flex';
});

function checkAdminPin() {
    const pin = document.getElementById('adminPin').value;
    if (pin === '2911') { // Admin specific PIN
        document.getElementById('adminModal').style.display = 'none';
        adminPanel.style.display = 'block';
        renderAdminLists();
    } else {
        document.getElementById('adminError').style.display = 'block';
    }
}

// Send attendance to Google Apps Script
function sendAttendance(type) {
    const worker = workerSelect.value;
    const workType = document.getElementById('work_type').value;
    const job = jobSelect.value;

    if(!worker || !workType || !job) {
        alert('Vyplňte prosím všechna pole.');
        return;
    }

    const record = {
        time: new Date().toLocaleString(),
        worker,
        workType,
        job,
        action: type
    };

    // Keep local log
    attendanceLog.push(record);
    saveToLocalStorage();

    const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbw7FyB80G6B5zXxizq1MolBYHIbidfQlMsEqgWTp-3h1YCyQNQwzlzzPS3BXwfAwfIj/exec';

    const payload = {
        action: type,
        worker: worker,
        team: workType,
        job: job
    };

    fetch(SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    }).then(() => {
        console.log('Sending to DB:', record);
        alert(`Záznam uložen!\n\nPracovník: ${worker}\nTyp: ${workType}\nZakázka: ${job}\nAkce: ${type === 'IN' ? 'PŘÍCHOD' : 'ODCHOD'}`);
        // Optional: clear selection
        workerSelect.value = '';
        document.getElementById('work_type').value = '';
        jobSelect.value = '';
    }).catch(err => {
        console.error('Error sending attendance', err);
        alert('Nepodařilo se odeslat záznam do tabulky, zkontrolujte připojení k internetu.');
    });
}

renderSelects();
