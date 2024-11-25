// Import the required testing utilities
import { describe, it, expect } from '@jest/globals';

// Example function to be tested
function add(a: number, b: number): number {
  return a + b;
}

// Test Suite
describe('Base Test Suite', () => {
  it('should add two numbers correctly', () => {
    const result = add(2, 3);
    expect(result).toBe(5); // Assertion
  });

  it('should handle adding zero correctly', () => {
    const result = add(4, 0);
    expect(result).toBe(4); // Assertion
  });

  it('should return a negative number when adding two negatives', () => {
    const result = add(-2, -3);
    expect(result).toBe(-5); // Assertion
  });
});

