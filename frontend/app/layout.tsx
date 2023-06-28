import './globals.css'
import { ReactNode } from 'react'
import Provider from './Provider'

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
