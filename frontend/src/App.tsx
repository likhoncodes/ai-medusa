import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Toaster } from "react-hot-toast"

// Components
import Layout from "./components/Layout"
import Dashboard from "./pages/Dashboard"
import BrowserAutomation from "./pages/BrowserAutomation"
import AIServices from "./pages/AIServices"
import Login from "./pages/Login"
import Register from "./pages/Register"

// Hooks
import { useAuthStore } from "./stores/authStore"

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Toaster position="top-right" />

          {isAuthenticated ? (
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/browser" element={<BrowserAutomation />} />
                <Route path="/ai" element={<AIServices />} />
              </Routes>
            </Layout>
          ) : (
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Login />} />
            </Routes>
          )}
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
