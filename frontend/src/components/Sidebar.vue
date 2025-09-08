<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h2 class="sidebar-title">Chat Sessions</h2>
      <button @click="createNewSession" class="new-session-btn">
        <PlusIcon class="w-4 h-4" />
        New Chat
      </button>
    </div>

    <div class="sessions-list">
      <div
        v-for="session in sessions"
        :key="session.id"
        :class="sessionItemClasses(session)"
        @click="selectSession(session.id)"
      >
        <div class="session-info">
          <h3 class="session-title">{{ session.title }}</h3>
          <p class="session-preview">{{ getLastMessage(session) }}</p>
          <span class="session-time">{{ formatTime(session.updated_at) }}</span>
        </div>
        <div class="session-actions">
          <button @click.stop="editSession(session)" class="action-btn">
            <EditIcon class="w-4 h-4" />
          </button>
          <button @click.stop="deleteSession(session.id)" class="action-btn delete-btn">
            <TrashIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">
          <UserIcon class="w-5 h-5" />
        </div>
        <div class="user-details">
          <span class="user-name">Developer</span>
          <span class="user-status">Online</span>
        </div>
      </div>
      <button @click="toggleSettings" class="settings-btn">
        <SettingsIcon class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { PlusIcon, EditIcon, TrashIcon, UserIcon, SettingsIcon } from 'lucide-vue-next'

interface ChatSession {
  id: string
  title: string
  updated_at: string
  messages: Array<{
    content: string
    type: string
  }>
}

interface Props {
  sessions: ChatSession[]
  activeSessionId?: string
}

interface Emits {
  (e: 'create-session'): void
  (e: 'select-session', sessionId: string): void
  (e: 'edit-session', session: ChatSession): void
  (e: 'delete-session', sessionId: string): void
  (e: 'toggle-settings'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const sessionItemClasses = (session: ChatSession) => [
  'session-item',
  {
    'session-active': props.activeSessionId === session.id
  }
]

const createNewSession = () => {
  emit('create-session')
}

const selectSession = (sessionId: string) => {
  emit('select-session', sessionId)
}

const editSession = (session: ChatSession) => {
  emit('edit-session', session)
}

const deleteSession = (sessionId: string) => {
  if (confirm('Are you sure you want to delete this session?')) {
    emit('delete-session', sessionId)
  }
}

const toggleSettings = () => {
  emit('toggle-settings')
}

const getLastMessage = (session: ChatSession) => {
  const lastMessage = session.messages[session.messages.length - 1]
  if (!lastMessage) return 'No messages yet'
  
  const content = lastMessage.content
  return content.length > 50 ? content.substring(0, 50) + '...' : content
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffHours / 24)

  if (diffHours < 1) return 'Just now'
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}
</script>

<style scoped>
.sidebar {
  @apply w-80 bg-gray-50 border-r border-gray-200 flex flex-col h-full;
}

.sidebar-header {
  @apply p-4 border-b border-gray-200;
}

.sidebar-title {
  @apply text-lg font-semibold text-gray-800 mb-3;
}

.new-session-btn {
  @apply w-full flex items-center justify-center gap-2 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors duration-200;
}

.sessions-list {
  @apply flex-1 overflow-y-auto;
}

.session-item {
  @apply flex items-center justify-between p-4 border-b border-gray-100 hover:bg-white cursor-pointer transition-colors duration-200;
}

.session-active {
  @apply bg-white border-l-4 border-l-blue-500;
}

.session-info {
  @apply flex-1 min-w-0;
}

.session-title {
  @apply font-medium text-gray-800 truncate;
}

.session-preview {
  @apply text-sm text-gray-600 truncate mt-1;
}

.session-time {
  @apply text-xs text-gray-500 mt-1;
}

.session-actions {
  @apply flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity;
}

.session-item:hover .session-actions {
  @apply opacity-100;
}

.action-btn {
  @apply p-2 text-gray-400 hover:text-gray-600 rounded;
}

.delete-btn:hover {
  @apply text-red-500;
}

.sidebar-footer {
  @apply p-4 border-t border-gray-200 flex items-center justify-between;
}

.user-info {
  @apply flex items-center gap-3;
}

.user-avatar {
  @apply w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center;
}

.user-details {
  @apply flex flex-col;
}

.user-name {
  @apply text-sm font-medium text-gray-800;
}

.user-status {
  @apply text-xs text-green-500;
}

.settings-btn {
  @apply p-2 text-gray-400 hover:text-gray-600 rounded;
}
</style>
