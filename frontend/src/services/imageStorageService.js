/**
 * Servicio de almacenamiento local de imágenes en IndexedDB
 * Guarda archivos con metadatos completos y base64
 */

const DB_NAME = 'DentalAI-Images'
const DB_VERSION = 1
const STORE_NAME = 'radiographs'

export class ImageStorageService {
  constructor() {
    this.db = null
  }

  /**
   * Inicializa la base de datos IndexedDB
   */
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        resolve(this.db)
      }

      request.onupgradeneeded = (event) => {
        const db = event.target.result
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          const store = db.createObjectStore(STORE_NAME, { keyPath: 'id' })
          store.createIndex('fileName', 'fileName', { unique: false })
          store.createIndex('createdAt', 'createdAt', { unique: false })
        }
      }
    })
  }

  /**
   * Guarda una imagen con sus metadatos
   */
  async saveImage(file, base64Content) {
    if (!this.db) await this.init()

    const imageRecord = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      fileName: file.name,
      mimeType: file.type,
      fileSize: file.size,
      base64: base64Content,
      originalFile: {
        name: file.name,
        type: file.type,
        lastModified: file.lastModified,
        size: file.size,
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([STORE_NAME], 'readwrite')
      const store = transaction.objectStore(STORE_NAME)
      const request = store.add(imageRecord)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        resolve({
          id: imageRecord.id,
          ...imageRecord,
        })
      }
    })
  }

  /**
   * Obtiene una imagen por ID
   */
  async getImage(id) {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([STORE_NAME], 'readonly')
      const store = transaction.objectStore(STORE_NAME)
      const request = store.get(id)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(request.result)
    })
  }

  /**
   * Obtiene todas las imágenes almacenadas
   */
  async getAllImages() {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([STORE_NAME], 'readonly')
      const store = transaction.objectStore(STORE_NAME)
      const index = store.index('createdAt')
      const request = index.getAll()

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        // Ordenar por fecha descendente (más recientes primero)
        const images = request.result.sort((a, b) =>
          new Date(b.createdAt) - new Date(a.createdAt)
        )
        resolve(images)
      }
    })
  }

  /**
   * Elimina una imagen por ID
   */
  async deleteImage(id) {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([STORE_NAME], 'readwrite')
      const store = transaction.objectStore(STORE_NAME)
      const request = store.delete(id)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(true)
    })
  }

  /**
   * Elimina todas las imágenes
   */
  async clearAll() {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([STORE_NAME], 'readwrite')
      const store = transaction.objectStore(STORE_NAME)
      const request = store.clear()

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(true)
    })
  }

  /**
   * Obtiene el tamaño total del almacenamiento
   */
  async getTotalSize() {
    const images = await this.getAllImages()
    let totalSize = 0

    for (const image of images) {
      if (image.base64) {
        // Aproximación: cada carácter en base64 ocupa 1 byte
        totalSize += image.base64.length
      }
    }

    return totalSize
  }

  /**
   * Descarga una imagen como archivo
   */
  downloadImage(image) {
    try {
      // Convertir base64 a blob
      const byteCharacters = atob(image.base64)
      const byteNumbers = new Array(byteCharacters.length)
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      const blob = new Blob([byteArray], { type: image.mimeType })

      // Crear enlace de descarga
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = image.fileName
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)

      return true
    } catch (error) {
      console.error('Error descargando imagen:', error)
      return false
    }
  }

  /**
   * Exporta una imagen como JSON con metadatos
   */
  exportAsJSON(image) {
    const exportData = {
      metadata: {
        id: image.id,
        fileName: image.fileName,
        mimeType: image.mimeType,
        fileSize: image.fileSize,
        createdAt: image.createdAt,
        updatedAt: image.updatedAt,
      },
      base64: image.base64,
    }

    const dataStr = JSON.stringify(exportData, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${image.id}-metadata.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }
}

// Instancia singleton
const imageStorageService = new ImageStorageService()
export default imageStorageService

