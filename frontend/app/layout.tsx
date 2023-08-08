import './globals.css'
import { ReactNode } from 'react'
import Provider from './Provider'
import Header from './components/Header/Header'

interface IProps {
  children: ReactNode;
}

export default function RootLayout({
  children,
}: IProps) {
  return (
    <html lang="en">
      <body>
        <Provider>
           {children}
        </Provider>
      </body>
    </html>
  )
}
