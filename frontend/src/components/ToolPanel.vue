<template>
  <div class="tool-panel" :class="{ 'panel-open': isOpen }">
    <div class="panel-header">
      <h3 class="panel-title">Developer Tools</h3>
      <button @click="togglePanel" class="close-btn">
        <XIcon class="w-5 h-5" />
      </button>
    </div>

    <div class="panel-content">
      <div class="tool-section">
        <h4 class="section-title">Shell Commands</h4>
        <div class="shell-interface">
          <div class="command-input">
            <input
              v-model="shellCommand"
              @keydown.enter="executeShell"
              placeholder="Enter shell command..."
              class="shell-input"
            />
            <button @click="executeShell" :disabled="!shellCommand.trim()" class="execute-btn">
              <PlayIcon class="w-4 h-4" />
            </button>
          </div>
          <div v-if="shellOutput" class="shell-output">
            <pre>{{ shellOutput }}</pre>
          </div>
        </div>
      </div>

      <div class="tool-section">
        <h4 class="section-title">File Operations</h4>
        <div class="file-interface">
          <div class="file-controls">
            <select v-model="fileOperation" class="operation-select">
              <option value="read">Read</option>
              <option value="write">Write</option>
              <option value="delete">Delete</option>
              <option value="list">List</option>
            </select>
            <input
              v-model="filePath"
              placeholder="File path..."
              class="path-input"
            />
          </div>
          <textarea
            v-if="fileOperation === 'write'"
            v-model="fileContent"
            placeholder="File content..."
            class="content-textarea"
            rows="4"
          />
          <button @click="executeFileOperation" class="execute-btn">
            <FileIcon class="w-4 h-4" />
            Execute
          </button>
          <div v-if="fileOutput" class="file-output">
            <pre>{{ fileOutput }}</pre>
          </div>
        </div>
      </div>

      <div class="tool-section">
        <h4 class="section-title">System Monitor</h4>
        <div class="monitor-interface">
          <div class="monitor-stats">
            <div class="stat-item">
              <span class="stat-label">CPU Usage:</span>
              <span class="stat-value">{{ systemStats.cpu }}%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Memory:</span>
              <span class="stat-value">{{ systemStats.memory }}%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Active Sessions:</span>
              <span class="stat-value">{{ systemStats.sessions }}</span>
            </div>
          </div>
          <button @click="refreshStats" class="refresh-btn">
            <RefreshCwIcon class="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { XIcon, PlayIcon, FileIcon, RefreshCwIcon } from 'lucide-vue-next'

interface Props {
  isOpen: boolean
}

interface Emits {
  (e: 'toggle-panel'): void
  (e: 'execute-shell', command: string): void
  (e: 'file-operation', operation: string, path: string, content?: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const shellCommand = ref('')
const shellOutput = ref('')
const fileOperation = ref('read')
const filePath = ref('')
const fileContent = ref('')
const fileOutput = ref('')

const systemStats = reactive({
  cpu: 45,
  memory: 62,
  sessions: 3
})

const togglePanel = () => {
  emit('toggle-panel')
}

const executeShell = () => {
  if (shellCommand.value.trim()) {
    emit('execute-shell', shellCommand.value.trim())
    shellOutput.value = `Executing: ${shellCommand.value}`
    shellCommand.value = ''
  }
}

const executeFileOperation = () => {
  if (filePath.value.trim()) {
    emit('file-operation', fileOperation.value, filePath.value, fileContent.value)
    fileOutput.value = `${fileOperation.value} operation on ${filePath.value}`
  }
}

const refreshStats = () => {
  // Simulate stats refresh
  systemStats.cpu = Math.floor(Math.random() * 100)
  systemStats.memory = Math.floor(Math.random() * 100)
  systemStats.sessions = Math.floor(Math.random() * 10) + 1
}
</script>

<style scoped>
.tool-panel {
  @apply fixed right-0 top-0 h-full w-96 bg-white border-l border-gray-200 transform translate-x-full transition-transform duration-300 z-50;
}

.panel-open {
  @apply translate-x-0;
}

.panel-header {
  @apply flex items-center justify-between p-4 border-b border-gray-200;
}

.panel-title {
  @apply text-lg font-semibold text-gray-800;
}

.close-btn {
  @apply p-2 text-gray-400 hover:text-gray-600 rounded;
}

.panel-content {
  @apply p-4 overflow-y-auto h-full;
}

.tool-section {
  @apply mb-6;
}

.section-title {
  @apply text-sm font-medium text-gray-700 mb-3;
}

.shell-interface, .file-interface, .monitor-interface {
  @apply space-y-3;
}

.command-input, .file-controls {
  @apply flex gap-2;
}

.shell-input, .path-input {
  @apply flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.operation-select {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.content-textarea {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none;
}

.execute-btn, .refresh-btn {
  @apply flex items-center gap-2 px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-200 disabled:bg-gray-300;
}

.shell-output, .file-output {
  @apply bg-gray-900 text-green-400 p-3 rounded-md text-sm font-mono max-h-32 overflow-y-auto;
}

.monitor-stats {
  @apply space-y-2;
}

.stat-item {
  @apply flex justify-between items-center;
}

.stat-label {
  @apply text-sm text-gray-600;
}

.stat-value {
  @apply text-sm font-medium text-gray-800;
}
</style>
