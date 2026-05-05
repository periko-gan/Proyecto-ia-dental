const DB_NAME = 'dental-ai-upload-queue'
const DB_VERSION = 1
const STORE_NAME = 'files'

function isIndexedDbAvailable() {
  return typeof window !== 'undefined' && 'indexedDB' in window
}

function requestToPromise(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error ?? new Error('IndexedDB request failed'))
  })
}

function openDatabase() {
  if (!isIndexedDbAvailable()) {
    return Promise.reject(new Error('IndexedDB no está disponible en este entorno.'))
  }

  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, DB_VERSION)

    request.onupgradeneeded = () => {
      const db = request.result
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id' })
      }
    }

    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error ?? new Error('No se pudo abrir IndexedDB.'))
  })
}

function normalizeStoredRecord(record) {
  if (!record) {
    return null
  }

  const rawFile = record.file
  const isFileLike = typeof File !== 'undefined' && rawFile instanceof File
  const isBlobLike = typeof Blob !== 'undefined' && rawFile instanceof Blob

  let file = rawFile
  if (!isFileLike && isBlobLike) {
    file = new File([rawFile], record.name, {
      type: record.type,
      lastModified: record.lastModified,
    })
  } else if (!isFileLike && rawFile) {
    file = new File([rawFile], record.name, {
      type: record.type,
      lastModified: record.lastModified,
    })
  }

  return {
    id: record.id,
    file,
    createdAt: record.createdAt ?? Date.now(),
  }
}

async function loadQueuedFiles() {
  const db = await openDatabase()
  try {
    const tx = db.transaction(STORE_NAME, 'readonly')
    const store = tx.objectStore(STORE_NAME)
    const records = await requestToPromise(store.getAll())

    return records
      .map(normalizeStoredRecord)
      .filter(Boolean)
      .sort((left, right) => (left.createdAt ?? 0) - (right.createdAt ?? 0))
  } finally {
    db.close()
  }
}

async function replaceQueuedFiles(entries) {
  const db = await openDatabase()
  try {
    const tx = db.transaction(STORE_NAME, 'readwrite')
    const store = tx.objectStore(STORE_NAME)

    await requestToPromise(store.clear())

    for (const entry of entries) {
      await requestToPromise(
        store.put({
          id: entry.id,
          file: entry.file,
          createdAt: entry.createdAt ?? Date.now(),
        }),
      )
    }
  } finally {
    db.close()
  }
}

async function clearQueuedFiles() {
  const db = await openDatabase()
  try {
    const tx = db.transaction(STORE_NAME, 'readwrite')
    const store = tx.objectStore(STORE_NAME)
    await requestToPromise(store.clear())
  } finally {
    db.close()
  }
}

export default {
  loadQueuedFiles,
  replaceQueuedFiles,
  clearQueuedFiles,
}


