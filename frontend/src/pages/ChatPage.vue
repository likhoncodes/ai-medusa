<template>
  <div class="chat-page">
    <Sidebar
      :sessions="sessions"
      :active-session-id="activeSessionId"
      @create-session="createSession"
      @select-session="selectSession"
      @edit-session="editSession"
      @delete-session="deleteSession"
      @toggle-settings="toggleSettings"
    />

    <div class="chat-main">
      <div class="chat-header">
        <h1 class="chat-title">{{ currentSession?.title || 'Select a chat' }}</h1>
        <div class="header-actions">
          <button @click="toggleTools" class="tool-toggle-btn">
            <WrenchIcon class="w-5 h-5" />
            Tools
          </button>
        </div>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-if="!currentSession" class="empty-state">
          <div class="empty-content">
            <MessageCircleIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-600 mb-2">No chat selected</h3>
            <p class="text-gray-500">Select a chat from the sidebar or create a new one to get started.</p>
          </div>
        </div>

        <div v-else>
          <ChatMessage
            v-for="message in currentSession.messages"
            :key="message.id"
            :message="message"
            @regenerate="regenerateMessage"
          />
        </div>

        <div v-if="isLoading" class="loading-indicator">
          <div class="loading-content">
            <LoaderIcon class="w-6 h-6 animate-spin text-blue-500" />
            <span class="text-gray-600">AI is thinking...</span>
          </div>
        </div>
      </div>

      <ChatInput
        :is-loading="isLoading"
        @send-message="sendMessage"
        @toggle-tools="toggleTools"
      />
    </div>

    <ToolPanel
      :is-open="showTools"
      @toggle-panel="toggleTools"
      @execute-shell="executeShell"
      @file-operation="fileOperation"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { MessageCircleIcon, WrenchIcon, LoaderIcon } from 'lucide-vue-next'
import Sidebar from '../components/Sidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'
import ToolPanel from '../components/ToolPanel.vue'
import { chatApi } from '../services/api'

interface ChatSession {
  id: string
  title: string
  created_at: string
  updated_at: string
  messages: Array<{
    id: string
    type: string
    content: string
    timestamp: string
    status: string
    metadata?: Record<string, any>
  }>
  context: Record<string, any>
  is_active: boolean
}

const sessions = ref<ChatSession[]>([])
const activeSessionId = ref<string>()
const isLoading = ref(false)
const showTools = ref(false)
const messagesContainer = ref<HTMLElement>()

const currentSession = computed(() => 
  sessions.value.find(s => s.id === activeSessionId.value)
)

onMounted(async () => {
  await loadSessions()
})

const loadSessions = async () => {
  try {
    sessions.value = await chatApi.getSessions()
    if (sessions.value.length > 0 && !activeSessionId.value) {
      activeSessionId.value = sessions.value[0].id
    }
  } catch (error) {
    console.error('Failed to load sessions:', error)
  }
}

const createSession = async () => {
  try {
    const newSession = await chatApi.createSession('New Chat')
    sessions.value.unshift(newSession)
    activeSessionId.value = newSession.id
  } catch (error) {
    console.error('Failed to create session:', error)
  }
}

const selectSession = (sessionId: string) => {
  activeSessionId.value = sessionId
}

const editSession = (session: ChatSession) => {
  const newTitle = prompt('Enter new title:', session.title)
  if (newTitle && newTitle.trim()) {
    session.title = newTitle.trim()
    // TODO: Update session on server
  }
}

const deleteSession = async (sessionId: string) => {
  try {
    await chatApi.deleteSession(sessionId)
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
    if (activeSessionId.value === sessionId) {
      activeSessionId.value = sessions.value[0]?.id
    }
  } catch (error) {
    console.error('Failed to delete session:', error)
  }
}

const sendMessage = async (content: string) => {
  if (!activeSessionId.value) return

  try {
    isLoading.value = true
    const response = await chatApi.sendMessage(activeSessionId.value, content)
    
    // Reload session to get updated messages
    const updatedSession = await chatApi.getSession(activeSessionId.value)
    const sessionIndex = sessions.value.findIndex(s => s.id === activeSessionId.value)
    if (sessionIndex !== -1 && updatedSession) {
      sessions.value[sessionIndex] = updatedSession
    }
    
    await scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    isLoading.value = false
  }
}

const regenerateMessage = async (messageId: string) => {
  // TODO: Implement message regeneration
  console.log('Regenerate message:', messageId)
}

const executeShell = async (command: string) => {
  try {
    const result = await chatApi.executeShell(command)
    console.log('Shell result:', result)
  } catch (error) {
    console.error('Shell execution failed:', error)
  }
}

const fileOperation = async (operation: string, path: string, content?: string) => {
  try {
    const result = await chatApi.fileOperation(operation, path, content)
    console.log('File operation result:', result)
  } catch (error) {
    console.error('File operation failed:', error)
  }
}

const toggleTools = () => {
  showTools.value = !showTools.value
}

const toggleSettings = () => {
  // TODO: Implement settings panel
  console.log('Toggle settings')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-page {
  @apply flex h-screen bg-gray-50;
}

.chat-main {
  @apply flex-1 flex flex-col;
}

.chat-header {
  @apply flex items-center justify-between p-4 bg-white border-b border-gray-200;
}

.chat-title {
  @apply text-xl font-semibold text-gray-800;
}

.header-actions {
  @apply flex gap-2;
}

.tool-toggle-btn {
  @apply flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors duration-200;
}

.chat-messages {
  @apply flex-1 overflow-y-auto p-4;
}

.empty-state {
  @apply flex items-center justify-center h-full;
}

.empty-content {
  @apply text-center;
}

.loading-indicator {
  @apply flex justify-center py-4;
}

.loading-content {
  @apply flex items-center gap-2;
}
</style>
