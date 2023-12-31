import {
        useReactTable,
        flexRender,
        getCoreRowModel
        } from "@tanstack/react-table";

const TableSimple = ({data, columns}) => {

        const table = useReactTable({
                columns,
                data,
                getCoreRowModel: getCoreRowModel(),
        });

        return (
        <div>
                <table>
                      <thead>
                        {table.getHeaderGroups().map(headerGroup => (
                          <tr key={headerGroup.id}>
                            {headerGroup.headers.map(header => (
                              <th key={header.id}>
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
                          <tr key={row.id}>
                            {row.getVisibleCells().map(cell => (
                              <td key={cell.id}>
                                {flexRender(cell.column.columnDef.cell, cell.getContext())}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                      <tfoot>
                        {table.getFooterGroups().map(footerGroup => (
                          <tr key={footerGroup.id}>
                            {footerGroup.headers.map(header => (
                              <th key={header.id}>
                                {header.isPlaceholder
                                  ? null
                                  : flexRender(
                                      header.column.columnDef.footer,
                                      header.getContext()
                                    )}
                              </th>
                            ))}
                          </tr>
                        ))}
                      </tfoot>
                </table>
        </div>
        )
}

export default TableSimple
