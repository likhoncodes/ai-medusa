const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"

class ChatAPI {
  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  async getSessions() {
    return this.request("/sessions")
  }

  async getSession(sessionId: string) {
    return this.request(`/sessions/${sessionId}`)
  }

  async createSession(title = "New Chat") {
    return this.request("/sessions", {
      method: "POST",
      body: JSON.stringify({ title }),
    })
  }

  async sendMessage(sessionId: string, content: string) {
    return this.request(`/sessions/${sessionId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    })
  }

  async deleteSession(sessionId: string) {
    return this.request(`/sessions/${sessionId}`, {
      method: "DELETE",
    })
  }

  async executeShell(command: string) {
    return this.request("/sandbox/shell", {
      method: "POST",
      body: JSON.stringify({ command }),
    })
  }

  async fileOperation(operation: string, path: string, content?: string) {
    return this.request("/sandbox/file", {
      method: "POST",
      body: JSON.stringify({ operation, path, content }),
    })
  }
}

export const chatApi = new ChatAPI()
