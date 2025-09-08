<template>
  <div :class="messageClasses">
    <div v-if="message.type === 'user'" class="user-message">
      <div class="message-avatar">
        <UserIcon class="w-5 h-5" />
      </div>
      <div class="message-content">
        <div class="message-text">{{ message.content }}</div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>

    <div v-else-if="message.type === 'assistant'" class="assistant-message">
      <div class="message-avatar">
        <BotIcon class="w-5 h-5" />
      </div>
      <div class="message-content">
        <div class="message-text" v-html="formatContent(message.content)"></div>
        <div class="message-actions">
          <button @click="copyMessage" class="action-btn">
            <CopyIcon class="w-4 h-4" />
          </button>
          <button @click="regenerateMessage" class="action-btn">
            <RefreshIcon class="w-4 h-4" />
          </button>
        </div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>

    <div v-else-if="message.type === 'tool'" class="tool-message">
      <div class="message-avatar">
        <WrenchIcon class="w-5 h-5" />
      </div>
      <div class="message-content">
        <div class="tool-header">
          <span class="tool-name">{{ getToolName(message) }}</span>
          <span :class="statusClasses">{{ message.status }}</span>
        </div>
        <div class="message-text">{{ message.content }}</div>
        <div v-if="message.metadata?.result" class="tool-result">
          <pre>{{ JSON.stringify(message.metadata.result, null, 2) }}</pre>
        </div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>

    <div v-else class="system-message">
      <div class="message-content">
        <div class="message-text">{{ message.content }}</div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { UserIcon, BotIcon, WrenchIcon, CopyIcon, RefreshIcon } from 'lucide-vue-next'

interface Message {
  id: string
  type: 'user' | 'assistant' | 'tool' | 'system'
  content: string
  timestamp: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  metadata?: Record<string, any>
}

interface Props {
  message: Message
}

interface Emits {
  (e: 'regenerate', messageId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const messageClasses = computed(() => [
  'message-container',
  `message-${props.message.type}`,
  `status-${props.message.status}`
])

const statusClasses = computed(() => [
  'status-badge',
  {
    'status-pending': props.message.status === 'pending',
    'status-processing': props.message.status === 'processing',
    'status-completed': props.message.status === 'completed',
    'status-error': props.message.status === 'error'
  }
])

const formatTimestamp = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString()
}

const formatContent = (content: string) => {
  // Basic markdown-like formatting
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

const getToolName = (message: Message) => {
  return message.metadata?.tool_name || 'Unknown Tool'
}

const copyMessage = async () => {
  try {
    await navigator.clipboard.writeText(props.message.content)
  } catch (err) {
    console.error('Failed to copy message:', err)
  }
}

const regenerateMessage = () => {
  emit('regenerate', props.message.id)
}
</script>

<style scoped>
.message-container {
  @apply mb-6;
}

.user-message, .assistant-message, .tool-message {
  @apply flex gap-3;
}

.system-message {
  @apply flex justify-center;
}

.message-avatar {
  @apply w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0;
}

.user-message .message-avatar {
  @apply bg-blue-500 text-white;
}

.assistant-message .message-avatar {
  @apply bg-green-500 text-white;
}

.tool-message .message-avatar {
  @apply bg-purple-500 text-white;
}

.message-content {
  @apply flex-1 min-w-0;
}

.message-text {
  @apply text-gray-800 leading-relaxed;
}

.message-actions {
  @apply flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity;
}

.action-btn {
  @apply p-1 text-gray-400 hover:text-gray-600 rounded;
}

.message-timestamp {
  @apply text-xs text-gray-500 mt-2;
}

.tool-header {
  @apply flex items-center justify-between mb-2;
}

.tool-name {
  @apply font-medium text-purple-700;
}

.status-badge {
  @apply px-2 py-1 rounded-full text-xs font-medium;
}

.status-pending {
  @apply bg-yellow-100 text-yellow-800;
}

.status-processing {
  @apply bg-blue-100 text-blue-800;
}

.status-completed {
  @apply bg-green-100 text-green-800;
}

.status-error {
  @apply bg-red-100 text-red-800;
}

.tool-result {
  @apply bg-gray-50 rounded-lg p-3 mt-2;
}

.tool-result pre {
  @apply text-sm text-gray-700 whitespace-pre-wrap;
}

.system-message .message-content {
  @apply bg-gray-100 rounded-lg px-4 py-2 text-sm text-gray-600;
}
</style>
