import hashlib
import json
import math

def _isCellAHint(grid, row, column):
    isHint = False
    gridArray = json.loads(grid)
    indexInGrid = (9 * (row - 1)) + (column - 1)
    if (int(gridArray[indexInGrid]) < 0):
        isHint = True 
        return isHint
    return isHint

def _insertValue(grid, value, row, col):
    gridArray = json.loads(grid)
    indexInGrid = (9 * (row - 1)) + col
    gridArray[indexInGrid - 1] = value
    return gridArray

def _calculateHash(grid):
    matrix = [[0 for rowNum in range(9)] for colNum in range(9)]
    strToBeHashed = ""
    gridArray = json.loads(grid)
    gridIndex = 0
    for rowIndex in range(9):
        for columnIndex in range(9):
            matrix[rowIndex][columnIndex] = gridArray[gridIndex]
            gridIndex+=1
    for columnIndex in range(9):
        for rowIndex in range(9):
            strToBeHashed += str(matrix[rowIndex][columnIndex])
    hashValue = hashlib.sha256()
    encodedStr = strToBeHashed.encode()
    hashValue.update(encodedStr)
    strToReturn = hashValue.hexdigest()
    return strToReturn


def _isValidGrid(grid):
    isGrid = True
    for entry in grid:
        if entry.isalpha():
            isGrid = False
            return isGrid
    gridArray = json.loads(grid)
    if len(gridArray) != 81:
        isGrid = False 
        return isGrid
    return isGrid

def _insert(parms):
    result = {'status': 'ok'}
    
  
    if 'cell' not in parms:
        result['status'] = 'hata: eksik hücre adresi'
        return result
    if len(parms['cell']) != 4:
        result['status'] = 'hata: geçersiz hücre adresi'
        return result
    if not parms['cell'][1].isnumeric() or not parms['cell'][3].isnumeric():
        result['status'] = 'hata: geçersiz hücre adresi'
        return result
    if parms['cell'][0] not in ('r', 'R') or parms['cell'][2] not in ('c', 'C'):
        result['status'] = 'hata: geçersiz hücre adresi'
        return result 
    if int(parms['cell'][1]) < 1 or int(parms['cell'][3]) < 1:
        result['status'] = 'hata: geçersiz hücre adresi'
        return result
    calculatedIntegrity = _calculateHash(parms['grid'])
    if (calculatedIntegrity != parms['integrity']):
        result['status'] = 'hata: hatalı integrity değeri'
        return result
    rowNumber = int(parms['cell'][1])
    columnNumber = int(parms['cell'][3])
    if 'grid' not in parms:
        result['status'] = 'hata: eksik grid'
        return result
    if not _isValidGrid(parms['grid']):
        result['status'] = 'hata: hatalı grid'
        return result
    
    rowNumber = int(parms['cell'][1])
    columnNumber = int(parms['cell'][3])

    if _isCellAHint(parms['grid'], rowNumber, columnNumber):
        result['status'] = 'hata: sabit olarak belirlenmiş bir hücreye değer ekleme girişiminde bulunuldu'
        return result

    if 'value' in parms:
        returnGrid = _insertValue(parms['grid'], int(parms['value']), rowNumber, columnNumber)
        result['grid'] = returnGrid
        result['status'] = 'ok'
        gridToHash = json.dumps(returnGrid)
        result['integrity'] = _calculateHash(gridToHash)
    else:
        result['status'] = 'hata: eksik parametre'

    return result

