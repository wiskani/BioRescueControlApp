import {
        useReactTable,
        flexRender,
        getCoreRowModel,
        ColumnDef,
        } from "@tanstack/react-table";

interface TableProps<T> {
        data: T[];
        columns: ColumnDef<any, any>[];
}

export function  TableSimple <T>({ data, columns }: TableProps<T>) { 

        const table = useReactTable({
                columns,
                data,
                getCoreRowModel: getCoreRowModel(),
        });

        return (
        <>
        <div className="relative overflow-x-auto">
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                      <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        {table.getHeaderGroups().map(headerGroup => (
                          <tr key={headerGroup.id}>
                            {headerGroup.headers.map(header => (
                              <th key={header.id} scope="col" className="px-6 py-3">
                                {header.isPlaceholder
                                  ? null
                                  : flexRender(
                                      header.column.columnDef.header,
                                      header.getContext()
                                    )}
                              </th>
                            ))}
                          </tr>
                        ))}
                      </thead>
                      <tbody>
                        {table.getRowModel().rows.map(row => (
                          <tr key={row.id} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            {row.getVisibleCells().map(cell => (
                              <td key={cell.id} className="px-6 py-4">
                                {flexRender(cell.column.columnDef.cell, cell.getContext())}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                </table>
        </div>
        </>
        )
}

