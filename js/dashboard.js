// ===== DASHBOARD FUNCTIONS =====

// Tab Switching
function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all sidebar links
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked link
    event.target.closest('.sidebar-link').classList.add('active');
    
    // Prevent default anchor behavior
    event.preventDefault();
}

// Filter Events
function filterEvents(status) {
    const rows = document.querySelectorAll('.event-row');
    const buttons = document.querySelectorAll('.filter-tab');
    
    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter rows
    rows.forEach(row => {
        if (status === 'all') {
            row.style.display = 'grid';
        } else {
            row.style.display = row.dataset.status === status ? 'grid' : 'none';
        }
    });
}

// Go to Event
function goToEvent(eventId) {
    window.location.href = `event-detail.html?id=${eventId}`;
}

// Download File
function downloadFile(filename) {
    showNotification(`Загрузка файла "${filename}"...`, 'success');
    console.log('Download:', filename);
}

// Logout
function logout() {
    if (confirm('Вы уверены, что хотите выйти?')) {
        showNotification('Выход выполнен', 'success');
        setTimeout(() => {
            window.location.href = '../index.html';
        }, 1000);
    }
}

// Admin Functions
function deleteUser(userId) {
    if (confirm('Вы уверены, что хотите удалить этого пользователя?')) {
        showNotification('Пользователь удален', 'success');
        // Remove row
        event.target.closest('.user-row').remove();
    }
}

function deleteEvent(eventId) {
    if (confirm('Вы уверены, что хотите удалить это мероприятие?')) {
        showNotification('Мероприятие удалено', 'success');
        event.target.closest('.admin-event-card').remove();
    }
}

function toggleEventStatus(eventId) {
    const badge = event.target.closest('.admin-event-card').querySelector('.event-badge');
    if (badge.textContent === 'Активно') {
        badge.textContent = 'Завершено';
        badge.className = 'event-badge status-completed';
        showNotification('Мероприятие завершено', 'success');
    } else {
        badge.textContent = 'Активно';
        badge.className = 'event-badge status-active';
        showNotification('Мероприятие активировано', 'success');
    }
}

// Jury Functions
function submitGrade(workId) {
    const gradeInput = document.querySelector(`#grade-${workId}`);
    const commentInput = document.querySelector(`#comment-${workId}`);
    
    if (!gradeInput || !commentInput) return;
    
    const grade = gradeInput.value;
    const comment = commentInput.value;
    
    if (!grade) {
        showNotification('Пожалуйста, укажите оценку', 'error');
        return;
    }
    
    if (!comment) {
        showNotification('Пожалуйста, добавьте комментарий', 'error');
        return;
    }
    
    showNotification('Оценка успешно отправлена!', 'success');
    
    // Update work status
    const workCard = event.target.closest('.work-card');
    if (workCard) {
        workCard.querySelector('.work-badge').textContent = 'Проверено';
        workCard.querySelector('.work-badge').className = 'work-badge status-completed';
    }
}

function viewWork(filename) {
    showNotification(`Открытие файла "${filename}"...`, 'success');
    console.log('View work:', filename);
}

// Teacher Functions
function viewStudentDetails(studentId) {
    showNotification('Переход к детальной информации ученика...', 'success');
    console.log('View student:', studentId);
}

function exportReport() {
    showNotification('Экспорт отчета...', 'success');
    console.log('Export report');
}

// Form Submissions
document.addEventListener('DOMContentLoaded', function() {
    // Profile form submission
    const profileForms = document.querySelectorAll('.profile-form');
    profileForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showNotification('Изменения сохранены!', 'success');
        });
    });
    
    // Event creation form
    const eventForm = document.querySelector('#createEventForm');
    if (eventForm) {
        eventForm.addEventListener('submit', function(e) {
            e.preventDefault();
            showNotification('Мероприятие успешно создано!', 'success');
            this.reset();
        });
    }
    
    // User creation form
    const userForm = document.querySelector('#createUserForm');
    if (userForm) {
        userForm.addEventListener('submit', function(e) {
            e.preventDefault();
            showNotification('Пользователь успешно создан!', 'success');
            this.reset();
        });
    }
});

// Initialize page
window.addEventListener('load', function() {
    // Show first tab by default
    const firstTab = document.querySelector('.tab-content');
    if (firstTab) {
        firstTab.classList.add('active');
    }
    
    // Activate first sidebar link
    const firstLink = document.querySelector('.sidebar-link');
    if (firstLink) {
        firstLink.classList.add('active');
    }
});

// Helper: Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ru-RU', options);
}

// Helper: Calculate days until
function daysUntil(dateString) {
    const target = new Date(dateString);
    const today = new Date();
    const diff = target - today;
    const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
    return days;
}

// Search functionality
function searchTable(inputId, tableSelector) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const rows = document.querySelectorAll(tableSelector);
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
