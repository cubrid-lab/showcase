import deck from './deck.json'

// Vite bundles recorded snapshots so deck.json selects the same data offline.
const snapshots = import.meta.glob('./snapshots/*.json', { eager: true, import: 'default' })
export const snapshot = snapshots[`./snapshots/${deck.snapshot}.json`]

if (!snapshot || snapshot.snapshotDate !== deck.snapshot) {
  throw new Error(`Missing or mismatched presentation snapshot: ${deck.snapshot}`)
}
