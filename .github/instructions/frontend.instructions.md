# Frontend Development Instructions

## Next.js App Router Patterns

### File Structure
\`\`\`
app/
├── layout.tsx          # Root layout with fonts and providers
├── page.tsx           # Homepage component
├── globals.css        # Global styles with Tailwind v4
└── api/              # API routes
    └── route.ts      # RESTful endpoints
\`\`\`

### Component Development

#### shadcn/ui Integration
- Always use existing UI components from `components/ui/`
- Extend components using the `cn()` utility for conditional styling
- Follow the established design token system

\`\`\`tsx
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export function CustomButton({ className, variant = "default", ...props }) {
  return (
    <Button 
      className={cn("custom-styles", className)} 
      variant={variant}
      {...props}
    />
  )
}
\`\`\`

#### TypeScript Patterns
- Define proper interfaces for all props and data structures
- Use generic types for reusable components
- Implement proper error boundaries

\`\`\`tsx
interface ComponentProps {
  title: string;
  data: ApiResponse<User[]>;
  onAction: (id: string) => Promise<void>;
}

export function DataComponent({ title, data, onAction }: ComponentProps) {
  // Implementation
}
\`\`\`

### Styling Guidelines

#### Tailwind CSS v4 Usage
- Use semantic design tokens: `bg-background`, `text-foreground`
- Implement responsive design with mobile-first approach
- Use the established color system with proper contrast ratios

\`\`\`tsx
<div className="bg-background text-foreground border border-border rounded-lg p-4">
  <h2 className="text-2xl font-bold text-balance mb-4">Title</h2>
  <p className="text-muted-foreground text-pretty">Description</p>
</div>
\`\`\`

### State Management
- Use React hooks for local state
- Implement proper loading and error states
- Use SWR for data fetching and caching

\`\`\`tsx
import useSWR from 'swr'

function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading } = useSWR(
    `/api/users/${userId}`,
    fetcher
  )

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error} />
  
  return <UserCard user={data} />
}
\`\`\`

### API Integration
- Use proper error handling for API calls
- Implement loading states and user feedback
- Follow RESTful conventions

\`\`\`tsx
async function handleSubmit(formData: FormData) {
  try {
    setLoading(true)
    const response = await fetch('/api/endpoint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
    
    if (!response.ok) throw new Error('Request failed')
    
    const result = await response.json()
    // Handle success
  } catch (error) {
    // Handle error
  } finally {
    setLoading(false)
  }
}
