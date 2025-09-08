<template>
  <div class="chat-input-container">
    <div class="input-wrapper">
      <textarea
        v-model="message"
        @keydown="handleKeyDown"
        @input="adjustHeight"
        ref="textareaRef"
        placeholder="Type your message..."
        class="message-input"
        :disabled="isLoading"
        rows="1"
      />
      <button
        @click="sendMessage"
        :disabled="!message.trim() || isLoading"
        class="send-button"
      >
        <SendIcon v-if="!isLoading" class="w-5 h-5" />
        <LoaderIcon v-else class="w-5 h-5 animate-spin" />
      </button>
    </div>
    <div class="input-actions">
      <button @click="clearInput" class="action-button">
        <TrashIcon class="w-4 h-4" />
        Clear
      </button>
      <button @click="toggleTools" class="action-button">
        <WrenchIcon class="w-4 h-4" />
        Tools
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { SendIcon, LoaderIcon, TrashIcon, WrenchIcon } from 'lucide-vue-next'

interface Props {
  isLoading?: boolean
}

interface Emits {
  (e: 'send-message', message: string): void
  (e: 'toggle-tools'): void
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false
})

const emit = defineEmits<Emits>()

const message = ref('')
const textareaRef = ref<HTMLTextAreaElement>()

const sendMessage = () => {
  if (message.value.trim() && !props.isLoading) {
    emit('send-message', message.value.trim())
    message.value = ''
    adjustHeight()
  }
}

const clearInput = () => {
  message.value = ''
  adjustHeight()
}

const toggleTools = () => {
  emit('toggle-tools')
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const adjustHeight = async () => {
  await nextTick()
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`
  }
}
</script>

<style scoped>
.chat-input-container {
  @apply border-t border-gray-200 bg-white p-4;
}

.input-wrapper {
  @apply flex items-end gap-3 mb-3;
}

.message-input {
  @apply flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent max-h-32 overflow-y-auto;
}

.message-input:disabled {
  @apply bg-gray-50 cursor-not-allowed;
}

.send-button {
  @apply bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg p-3 transition-colors duration-200;
}

.input-actions {
  @apply flex gap-2;
}

.action-button {
  @apply flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors duration-200;
}
</style>
