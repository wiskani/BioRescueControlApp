"use client";

import React from 'react'
import { useRouter } from 'next/navigation'

import { signIn, signOut, useSession } from 'next-auth/react'

export default function Home() {
    const { data: session } = useSession()
    console.log(session)
    const router = useRouter()

  return (
    <div>
            <div>
                <form >
                        <div >
                            <i ></i>
                            <input 
                            />
                        </div>
                        <div >
                            <i ></i>
                            <input
                            />
                        </div>
                        <button type="button" onClick={()=> router.push('/dashboard')}>
                            LOGIN
                        </button>
                        <a href="/">¿Olvidaste tu contraseña?</a>
                </form>
            </div>
        </div>
  )
}
