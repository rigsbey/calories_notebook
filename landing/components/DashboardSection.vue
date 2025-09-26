<template>
  <section class="dashboard-section">
    <div class="container">
      <div class="dashboard-preview">
        <div class="dashboard-header">
          <div class="dashboard-brand">
            <div class="brand-icon">🍽️</div>
            <span class="brand-text">Calories Bot</span>
          </div>
          <div class="dashboard-nav">
            <a href="#" class="dashboard-link">
              <span class="dashboard-icon">🏠</span>
              Dashboard
            </a>
          </div>
        </div>
        
        <div class="dashboard-content">
          <div class="dashboard-title">
            <span class="title-icon">📊</span>
            Nutrition Analysis
          </div>
          <div class="dashboard-subtitle">
            Next analysis in 2h 15m 30s
          </div>
          <div class="dashboard-description">
            AI-powered nutrition tracking from your food photos
          </div>
          
          <div class="dashboard-controls">
            <div class="control-group">
              <span class="control-label">Filter by:</span>
              <select class="control-select">
                <option>All Meals (12)</option>
              </select>
            </div>
            <div class="control-group">
              <span class="control-label">Sort by:</span>
              <select class="control-select">
                <option>Date</option>
              </select>
            </div>
            <div class="control-actions">
              <a href="#" class="control-action">
                <span class="action-icon">🔍</span>
                Find New Meals
              </a>
              <a href="#" class="control-action">
                <span class="action-icon">⚙️</span>
                Manage Settings
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.dashboard-section {
  @apply py-16;
  background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
  position: relative;
  overflow: hidden;
}

.dashboard-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  pointer-events: none;
}

.container {
  @apply max-w-6xl mx-auto px-6 relative z-10;
}

.dashboard-preview {
  @apply rounded-2xl shadow-2xl overflow-hidden;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.dashboard-header {
  @apply flex items-center justify-between p-6 border-b border-gray-200;
}

.dashboard-brand {
  @apply flex items-center space-x-3;
}

.brand-icon {
  @apply w-8 h-8 rounded-full flex items-center justify-center text-white text-lg;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3);
}

.brand-text {
  @apply text-xl font-bold text-gray-900;
}

.dashboard-nav {
  @apply flex items-center;
}

.dashboard-link {
  @apply flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors duration-300;
}

.dashboard-icon {
  @apply text-lg;
}

.dashboard-content {
  @apply p-6;
}

.dashboard-title {
  @apply flex items-center space-x-3 text-2xl font-bold text-gray-900 mb-2;
}

.title-icon {
  @apply text-2xl;
}

.dashboard-subtitle {
  @apply text-sm text-gray-500 mb-1;
}

.dashboard-description {
  @apply text-sm text-gray-500 mb-6;
}

.dashboard-controls {
  @apply flex items-center space-x-6 flex-wrap gap-4;
}

.control-group {
  @apply flex items-center space-x-2;
}

.control-label {
  @apply text-sm text-gray-700 font-medium;
}

.control-select {
  @apply bg-gray-100 border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
}

.control-actions {
  @apply flex items-center space-x-4 ml-auto;
}

.control-action {
  @apply flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 transition-colors duration-300;
}

.action-icon {
  @apply text-base;
}

@media (max-width: 768px) {
  .dashboard-controls {
    @apply flex-col items-start space-x-0 space-y-4;
  }
  
  .control-actions {
    @apply ml-0 w-full justify-start;
  }
}
</style>
