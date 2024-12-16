! gfortran two.f90 -fdefault-integer-8 -O2 -o run; time ./run <input-file>
program run
    implicit none

    integer :: i, sum
    integer, allocatable :: raw(:)

    call read_input(get_arg(1, 999), 999, raw)

    sum = 0
    do i = 1, size(raw)
        sum = sum + blink_cached(int(raw(i), 8), 75)
    end do
    write(*, *) sum
contains
    integer recursive function blink_cached(number, iterate) result(result)
        integer :: number, iterate, i, subnumbers(2)
        integer, parameter :: MAX_NUMBER = 1000, MAX_ITERATE = 75
        integer, dimension(0:MAX_ITERATE, 0:MAX_NUMBER), save :: hash_map
        logical, save :: initialized = .false.
        integer :: split_integer(2)
        logical :: applies

        if (.not. initialized) then
            initialized = .true.
            hash_map = -1
        end if

        if (number <= MAX_NUMBER .and. iterate <= MAX_ITERATE) then
            if (hash_map(iterate, number) > -1) then
                result = hash_map(iterate, number)
                return
            end if
        end if

        result = number
        do i = iterate, 1, -1
            if (result == 0) then
                result = 1
            else
                call process_case_2(result, applies, split_integer)
                if (applies) then
                    result = &
                        blink_cached(split_integer(1), i - 1) &
                        + blink_cached(split_integer(2), i - 1)
                    if (number <= MAX_NUMBER .and. iterate <= MAX_ITERATE) then
                        hash_map(iterate, number) = result
                    end if
                    return
                else
                    result = result * 2024
                end if
            end if
        end do
        result = 1
        if (number <= MAX_NUMBER .and. iterate <= MAX_ITERATE) then
            hash_map(iterate, number) = result
        end if
    end function
    subroutine process_case_2(value, applies, split_integer)
        integer :: value, ndigits
        integer, intent(out) :: split_integer(2)
        logical, intent(out) :: applies

        ndigits = floor(log10(float(value))) + 1

        applies = mod(ndigits, 2) == 0
        if (applies) then
            split_integer(1) = value / (10 ** (ndigits / 2))
            split_integer(2) = mod(value, 10 ** (ndigits / 2))
        end if
    end subroutine
    subroutine read_input(filename, max_buffer, result)
        integer :: max_buffer, fileunit, i, io
        character (*) :: filename
        integer, allocatable :: result(:)
        integer, dimension(max_buffer):: buffer

        ! initialize buffer
        buffer(:) = -1

        ! read data
        open(newunit=fileunit, file=filename)
        read(fileunit, *, iostat=io) buffer
        close(fileunit)

        ! find range
        do i = 1, max_buffer
            if (buffer(i) == -1) exit
        end do

        ! write result
        allocate(result(i-1))
        result = buffer(1:i-1)

    end subroutine
    function get_arg(n, max_length)
        integer :: n, max_length
        character(len=max_length) :: get_arg

        call get_command_argument(n, get_arg)
    end function
end program
