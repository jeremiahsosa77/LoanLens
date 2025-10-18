import { describe, it, expect } from 'vitest'

describe('App', () => {
  it('should pass basic test', () => {
    expect(true).toBe(true)
  })

  it('should calculate correctly', () => {
    const sum = 2 + 2
    expect(sum).toBe(4)
  })
})
