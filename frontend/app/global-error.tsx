'use client'

import { useEffect } from 'react'
 
export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
        useEffect(() => {
                console.error(`el error es: ${error}`)
        }, [error])
  return (
        <div>
        <h2>Algo salió mal</h2>
        <button
        onClick={
                ()=> reset()
                }
        >
       Intentarlo de nuevo      
        </button>



        </div>
  )
}
