const defaultWorkers = ['Pracovník 1', 'Pracovník 2', 'Pracovník 3', 'Pracovník 4'];
const defaultJobs = ['2026-06-001 Hořice', '2026-06-002 Lískovice 22', '2026-06-003 SVJ Hostinné'];

let workers = JSON.parse(localStorage.getItem('foxgarden_workers')) || defaultWorkers;
let jobs = JSON.parse(localStorage.getItem('foxgarden_jobs')) || defaultJobs;

const workerSelect = document.getElementById('worker');
const jobSelect = document.getElementById('job');
const workerList = document.getElementById('workerList');
const jobList = document.getElementById('jobList');
const adminPanel = document.getElementById('adminPanel');

// Init
function renderSelects() {
    workerSelect.innerHTML = '<option value="">-- vyber --</option>';
    workers.forEach(w => {
        workerSelect.innerHTML += `<option value="${w}">${w}</option>`;
    });

    jobSelect.innerHTML = '<option value="">-- vyber --</option>';
    jobs.forEach(j => {
        jobSelect.innerHTML += `<option value="${j}">${j}</option>`;
    });
}

function renderAdminLists() {
    workerList.innerHTML = '';
    workers.forEach((w, index) => {
        workerList.innerHTML += `<li style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee;">
            ${w} <button class="delete-btn" onclick="deleteWorker(${index})">Smazat</button>
        </li>`;
    });

    jobList.innerHTML = '';
    jobs.forEach((j, index) => {
        jobList.innerHTML += `<li style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #eee;">
            ${j} <button class="delete-btn" onclick="deleteJob(${index})">Smazat</button>
        </li>`;
    });
}

function saveToLocalStorage() {
    localStorage.setItem('foxgarden_workers', JSON.stringify(workers));
    localStorage.setItem('foxgarden_jobs', JSON.stringify(jobs));
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
        jobs.push(val);
        input.value = '';
        saveToLocalStorage();
    }
}

function deleteJob(index) {
    if(confirm('Opravdu smazat zakázku?')) {
        jobs.splice(index, 1);
        saveToLocalStorage();
    }
}

// Admin Auth
document.getElementById('btnAdmin').addEventListener('click', () => {
    document.getElementById('adminModal').style.display = 'flex';
});

function checkAdminPin() {
    const pin = document.getElementById('adminPin').value;
    if (pin === '1133') { // Simple admin PIN, same as entrance
        document.getElementById('adminModal').style.display = 'none';
        adminPanel.style.display = 'block';
        renderAdminLists();
    } else {
        document.getElementById('adminError').style.display = 'block';
    }
}

// Mock sending attendance
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

    console.log('Sending to DB:', record);
    alert(`Záznam uložen!\n\nPracovník: ${worker}\nTyp: ${workType}\nZakázka: ${job}\nAkce: ${type === 'IN' ? 'PŘÍCHOD' : 'ODCHOD'}`);
}

renderSelects();
