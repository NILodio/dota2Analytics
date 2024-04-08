import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_layout/dota')({
  component: () => <div>Hello /_layout/dota!</div>
})